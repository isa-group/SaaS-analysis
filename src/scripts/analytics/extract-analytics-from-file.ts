/**
 * ------------ Overview ------------
 * 
 * This script processes a pricing file to extract analytics and logs the results.
 * 
 * The script uses the `pricing4ts` library to analyze a pricing model provided in the input file.
 * It logs both the analytics and any errors encountered during processing into a dedicated log folder
 * within the `logs` directory, timestamped to ensure unique entries for each run.
 * 
 * ------------ Features ------------
 * 
 * - Creates a timestamped log folder in the `logs` directory to organize results and errors.
 * - Reads and processes a pricing model file specified via a command-line argument.
 * - Uses the `PricingService` class from the `pricing4ts` library to calculate analytics for the pricing model.
 * - Logs the analytics into `results.log` and errors into `errors.log` within the log folder.
 * 
 * ------------ Parameters ------------
 * 
 * - **filePath**: The path to the pricing file to process. This is passed as the first argument when running the script.
 * 
 * ------------ How to Run ------------
 * 
 * 1. Install the required dependencies, including `pricing4ts`.
 * 2. Use the following command to execute the script:
 * 
 *    ```bash
 *    npm run analytics-from-file <path-to-pricing-file>
 *    ```
 * 
 * Replace `<path-to-pricing-file>` with the path to the pricing file to analyze.
 * 
 * 3. The results and errors will be logged in a timestamped folder located in the `logs` directory.
 * 
 * ------------ Example ------------
 * 
 *    ```bash
 *    npm run analytics-from-file ../data/pricings/yaml/real-v2/microsoft365Business/2022.yml
 *    ```
 * 
 * In this example:
 * - The script processes `../data/pricings/yaml/real-v2/microsoft365Business/2022.yml`.
 * - Analytics will be saved in `results.log`, and any errors will be saved in `errors.log` within a log folder 
 *   in the `logs` directory, named with the corresponding timestamp of the run.
 */



import * as fs from 'fs';
import * as path from 'path';
import { Pricing } from 'pricing4ts';
import { PricingService, retrievePricingFromPath } from 'pricing4ts/server';

/**
 * Directory where log files are stored.
 * 
 * @constant {string}
 */
const LOG_DIR = 'logs';

/**
 * The directory path where log files for pricing analytics will be stored.
 * The folder name includes a timestamp to ensure uniqueness and avoid conflicts.
 * The timestamp format replaces colons and periods with hyphens to create a valid folder name.
 * @constant {string}
 */
const LOG_FOLDER = path.join(
    LOG_DIR,
    `pricing-analytics-${new Date().toISOString().replace(/[:.]/g, "-")}`
  );

/**
 * A writable stream for logging results to a file named 'results.log' located in the LOG_FOLDER directory.
 * The stream is opened in append mode, meaning new data will be added to the end of the file.
 *
 * @constant {WriteStream} resultsLogStream - The writable stream for logging results.
 */
const resultsLogStream = fs.createWriteStream(
    path.join(LOG_FOLDER, "results.log"),
    { flags: "a" }
  );
  
  /**
   * A writable stream for logging results to a file named 'results.log' located in the LOG_FOLDER directory.
   * The stream is opened in append mode, meaning new data will be added to the end of the file.
   *
   * @constant {WriteStream} resultsLogStream - The writable stream for logging results.
   */
  const errorsLogStream = fs.createWriteStream(
    path.join(LOG_FOLDER, "errors.log"),
    { flags: "a" }
  );

/**
 * Create the LOG_DIR directory if it does not exist.
 */
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR);
}

/**
 * Create the LOG_FOLDER directory if it does not exist.
 */
if (!fs.existsSync(LOG_FOLDER)) {
  fs.mkdirSync(LOG_FOLDER);
}

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
        const analytics = await pricingService.getAnalytics();
        resultsLogStream.write(`Analytics for ${filePath}:\n${JSON.stringify(analytics, null, 2)}\n\n`);
    } catch (error) {
        errorsLogStream.write(`Error processing file ${filePath}: ${(error as Error).message}\n\n`);
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

    processFile(filePath)
        .then(() => {
            resultsLogStream.end();
            errorsLogStream.end();

            // Remove empty log files
            if (fs.statSync(path.join(LOG_FOLDER, 'results.log')).size === 0) {
                fs.unlinkSync(path.join(LOG_FOLDER, 'results.log'));
            }
            if (fs.statSync(path.join(LOG_FOLDER, 'errors.log')).size === 0) {
                fs.unlinkSync(path.join(LOG_FOLDER, 'errors.log'));
            }
        })
        .catch(error => {
            console.error('Error processing file:', error);
            resultsLogStream.end();
            errorsLogStream.end();
        });
}

main();
