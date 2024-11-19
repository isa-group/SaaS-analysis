import * as fs from 'fs';
import * as path from 'path';
import { PricingService, Pricing, retrievePricingFromPath } from 'pricing4ts';
import cliProgress from 'cli-progress';

const DATA_DIR = 'data/pricings/yaml';
const LOG_DIR = 'logs';
const LOG_FILE = path.join(LOG_DIR, `pricing-analytics-${new Date().toISOString().replace(/[:.]/g, '-')}.log`);

if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}

const logStream = fs.createWriteStream(LOG_FILE, { flags: 'a' });

function getAllFiles(dir: string, fileList: string[] = []): string[] {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            getAllFiles(filePath, fileList);
        } else {
            fileList.push(filePath);
        }
    });
    return fileList;
}

async function processFile(filePath: string, progressBar: cliProgress.SingleBar) {
    try {
        const pricing: Pricing = retrievePricingFromPath(filePath);
        const pricingService = new PricingService(pricing);
        const analytics = await pricingService.getAnalytics();
        logStream.write(`Analytics for ${filePath}:\n${JSON.stringify(analytics, null, 2)}\n\n`);
    } catch (error) {
        logStream.write(`Error processing file ${filePath}: ${(error as Error).message}\n\n`);
    } finally {
        progressBar.increment();
    }
}

async function main() {
    const files = getAllFiles(DATA_DIR);
    const progressBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    progressBar.start(files.length, 0);

    await Promise.all(files.map(file => processFile(file, progressBar)));

    progressBar.stop();
    logStream.end();
}

main();