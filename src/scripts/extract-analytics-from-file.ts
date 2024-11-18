import * as fs from 'fs';
import * as path from 'path';
import { PricingService, Pricing, retrievePricingFromPath } from 'pricing4ts';

const LOG_DIR = 'logs';
const LOG_FILE = path.join(LOG_DIR, `pricing-analytics-${new Date().toISOString().replace(/[:.]/g, '-')}.log`);

if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}

const logStream = fs.createWriteStream(LOG_FILE, { flags: 'a' });

async function processFile(filePath: string) {
    try {
        const pricing: Pricing = retrievePricingFromPath(filePath);
        const pricingService = new PricingService(pricing);
        const analytics = await pricingService.getAnalytics();
        logStream.write(`Analytics for ${filePath}:\n${JSON.stringify(analytics, null, 2)}\n\n`);
    } catch (error) {
        console.error(`Error processing file ${filePath}:`, error);
        logStream.write(`Error processing file ${filePath}: ${(error as Error).message}\n\n`);
    }
}

function main() {
    const filePath = process.argv[2];
    if (!filePath) {
        console.error('Please provide a file path as an argument.');
        process.exit(1);
    }

    processFile(filePath)
        .then(() => {
            logStream.end();
        })
        .catch(error => {
            console.error('Error processing file:', error);
            logStream.end();
        });
}

main();
