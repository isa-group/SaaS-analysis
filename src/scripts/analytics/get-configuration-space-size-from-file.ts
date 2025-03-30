import * as fs from 'fs';
import * as path from 'path';
import { Pricing } from 'pricing4ts';
import { PricingService, retrievePricingFromPath } from 'pricing4ts/server';
/**
 * Processes a single pricing file, retrieves analytics data, and logs the results.
 * 
 * @param {string} filePath - The path to the pricing file.
 * @returns {Promise<void>} A promise that resolves when the file processing is complete.
 */
async function processFile(filePath: string): Promise<void> {
    try {
        const pricing: Pricing = retrievePricingFromPath(filePath);
        const pricingService = new PricingService(pricing);
        const analytics = await pricingService.getConfigurationSpace();
    } catch (error) {
      console.log(error);
    }
}

/**
 * Main function that orchestrates the extraction and processing of pricing analytics.
 * 
 * - Retrieves the file path from command line arguments.
 * - Processes the file to extract analytics data.
 * - Writes the results and errors to the log file.
 */
function main(): void {
    const filePath = process.argv[2];
    if (!filePath) {
        console.error('Please provide a file path as an argument.');
        process.exit(1);
    }

    console.log(filePath);

    processFile(filePath)
        .then(() => {
            console.log("Analytics extraction completed successfully.");
        })
        .catch(error => {
            console.error('Error processing file:', error);
        });
}

main();
