import * as fs from "fs";
import * as path from "path";
import { Pricing, retrievePricingFromPath } from "pricing4ts";
import { PricingOperation, PricingService } from "pricing4ts/server";
import cliProgress from "cli-progress";

interface Results {
    inconsistencies: number;
    noInconsistencies: number;
    details: {testCase: string, inconsistencyDetected: boolean, executionTime: number, error: string}[];
}

const DATA_DIR = "data/pricings/yaml/synthetic";
const LOG_DIR = "logs";
const LOG_FOLDER = path.join(
    LOG_DIR,
    `validation-${new Date().toISOString().replace(/[:.]/g, "-")}`
);

const summaryLogStream = fs.createWriteStream(
    path.join(LOG_FOLDER, "summary.log"),
    { flags: "a" }
);

const detailsLogStream = fs.createWriteStream(
    path.join(LOG_FOLDER, "details.log"),
    { flags: "a" }
);

if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}

if (!fs.existsSync(LOG_FOLDER)) {
    fs.mkdirSync(LOG_FOLDER);
}

function getAllFiles(dir: string, fileList: string[] = []): string[] {
    const files = fs.readdirSync(dir);
    files.forEach((file) => {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            getAllFiles(filePath, fileList);
        } else if (file.endsWith(".yml") || file.endsWith(".yaml")) {
            fileList.push(filePath);
        }
    });
    return fileList;
}

async function processFile(
    filePath: string,
    progressBar: cliProgress.SingleBar,
    results: { inconsistencies: number; noInconsistencies: number; details: any[] }
): Promise<void> {
    const startTime = Date.now();
    const testCase = path.basename(path.dirname(filePath));
    let inconsistencyDetected = false;
    let error = "";

    try {

        const pricing: Pricing = retrievePricingFromPath(filePath);
        const pricingService = new PricingService(pricing);


        const operationResult = await pricingService.runPricingOperation(PricingOperation.VALID_SUBSCRIPTION);
        
        if (operationResult.statistics.nSolutions === 0){
            throw new Error("No subscriptions available in the pricing")
        }else{
            results.noInconsistencies++;
        }
    } catch (e) {
        inconsistencyDetected = true;
        error = (e as Error).message
        results.inconsistencies++;
    } finally {
        const endTime = Date.now();
        const executionTime = endTime - startTime;
        results.details.push({
            testCase,
            inconsistencyDetected,
            executionTime,
            error
        });
        progressBar.increment();
    }
}

async function main(): Promise<void> {
    const files = getAllFiles(DATA_DIR);
    const progressBar = new cliProgress.SingleBar(
        {},
        cliProgress.Presets.shades_classic
    );
    progressBar.start(files.length, 0);

    const results: Results = {
        inconsistencies: 0,
        noInconsistencies: 0,
        details: [],
    };

    for (const file of files) {
        await processFile(file, progressBar, results);
    }

    progressBar.stop();

    const totalCases = results.inconsistencies + results.noInconsistencies;
    const avgExecutionTime =
        results.details.reduce((sum, detail) => sum + detail.executionTime, 0) /
        totalCases;

    const inconsistencyPercentage = ((results.inconsistencies / totalCases) * 100).toFixed(2);

    summaryLogStream.write(
        `+------------------------------------+-------------------------+\n` +
        `| Inconsistencies Found              | ${results.inconsistencies.toString().padEnd(24)}|\n` +
        `| Inconsistencies Not Found          | ${results.noInconsistencies.toString().padEnd(24)}|\n` +
        `| Total Test Cases                   | ${totalCases.toString().padEnd(24)}|\n` +
        `+------------------------------------+-------------------------+\n` +
        `| Avg Execution Time                 | ${avgExecutionTime.toFixed(2)} ms${''.padEnd(16)}|\n` +
        `| Inconsistency Detection Rate (IDR) | ${inconsistencyPercentage} % ${''.padEnd(16)}|\n` +
        `+------------------------------------+-------------------------+\n`
    );

    detailsLogStream.write(
        `+------------------------------------------------------+------------------------------------------------------+------------------------------------------------------+\n` +
        `| Test Case                                            | Inconsistency Detected                               | Execution Time (ms)                                  |\n` +
        `+------------------------------------------------------+------------------------------------------------------+------------------------------------------------------+\n`
    );

    results.details.forEach((detail) => {
        detailsLogStream.write(
            `| ${detail.testCase.padEnd(53)}| ${detail.inconsistencyDetected ? '✓'.padEnd(53) : 'x'.padEnd(53)}| ${detail.executionTime.toString().padEnd(53)}|\n`
        );
    });

    detailsLogStream.write(
        `+------------------------------------------------------+------------------------------------------------------+------------------------------------------------------+\n\n\n`
    );

    results.details.forEach((detail) => {
        if (detail.error !== ""){
            detailsLogStream.write(
                `----------- ${detail.testCase} -----------\n\n${detail.error}\n\n\n`
            );
        }
    });

    summaryLogStream.end();
    detailsLogStream.end();
}

main();