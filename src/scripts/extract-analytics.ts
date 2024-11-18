import * as fs from 'fs';
import * as path from 'path';
import { PricingService, Pricing, retrievePricingFromPath } from 'pricing4ts';

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

async function processFile(filePath: string) {
    try {
        const pricing: Pricing = retrievePricingFromPath(filePath);
        if (pricing.saasName === 'Microsoft 365 - For Business') {
            console.log("stop");
        }
        const pricingService = new PricingService(pricing);
        const analytics = await pricingService.getAnalytics();
        logStream.write(`Analytics for ${filePath}:\n${JSON.stringify(analytics, null, 2)}\n\n`);
    } catch (error) {
        console.error(`Error processing file ${filePath}:`, error);
        logStream.write(`Error processing file ${filePath}: ${(error as Error).message}\n\n`);
    }
}

function main() {
    const files = getAllFiles(DATA_DIR);
    Promise.all(files.map(file => processFile(file)))
        .then(() => {
            logStream.end();
        })
        .catch(error => {
            console.error('Error processing files:', error);
            logStream.end();
        });
}

main();