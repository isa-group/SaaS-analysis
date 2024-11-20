/**
 * ------------ Overview ------------
 * This script processes multiple Pricing2Yaml files to extract analytics and logs the results.
 * 
 * The script recursively scans the specified data directory (data/pricings/yaml/real/) for pricing files, processes each file
 * using the `pricing4ts` library, and generates analytics for each SaaS pricing. The results
 * and any errors encountered during the process are logged into separate files in a timestamped
 * directory within the `logs` folder.
 * 
 * ------------ Features ------------
 * - Recursively scans the `data/pricings/yaml/real/` directory to find all pricing files.
 * - Uses a progress bar to display the processing status.
 * - Analyzes each pricing file with the `PricingService` from the `pricing4ts` library.
 * - Logs analytics and errors into separate files for clarity.
 * - Organizes analytics by SaaS name and date for structured output.
 * 
 * ------------ Parameters ------------
 * - **DATA_DIR**: Specifies the directory containing the pricing files to be processed.
 * - **LOG_DIR**: Specifies the base directory for storing log files.
 * - **LOG_FOLDER**: A subdirectory within `LOG_DIR`, timestamped to ensure uniqueness.
 * 
 * ------------ How to Run ------------
 * 1. Place the pricing YAML files to be analyzed in the `data/pricings/yaml` directory.
 * 2. Install the required dependencies, including `pricing4ts` and `cli-progress`.
 * 3. Run the script using Node.js:
 * 
 *    ```bash
 *    npm run analytics
 *    ```
 * 
 * 4. The progress bar will display the processing status.
 * 5. Results will be saved in a log file named `results.log`, and any errors will be saved in `errors.log`,
 *    both located in a timestamped folder within the `logs` directory.
 * 
 * ------------ Example ------------
 * If the `data/pricings/yaml/real` directory contains files like `example1.yml` and `example2.yml`,
 * running the script will:
 * - Process each file to extract analytics.
 * - Generate a structured log file in a folder named `pricing-analytics-<timestamp>` within the `logs` directory.
 * - Save errors (if any) in a separate file for debugging purposes.
 * 
 * ------------ Notes ------------
 * - Ensure that the directory structure and file permissions are correctly configured.
 * - The script assumes all files in the target directory are valid YAML files.
 * - Large datasets may take longer to process, as all files are processed in parallel.
 */


import * as fs from 'fs';
import * as path from 'path';
import { PricingService, Pricing, retrievePricingFromPath } from 'pricing4ts';
import cliProgress from 'cli-progress';

/**
 * The directory path where pricing YAML files are stored.
 * This constant is used to specify the location of the data files
 * that will be processed by the analytics extraction script.
 * @constant {string}
 */
const DATA_DIR = 'data/pricings/yaml/real';

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
const LOG_FOLDER = path.join(LOG_DIR, `pricing-analytics-${new Date().toISOString().replace(/[:.]/g, '-')}`);

/**
 * A writable stream for logging results to a file named 'results.log' located in the LOG_FOLDER directory.
 * The stream is opened in append mode, meaning new data will be added to the end of the file.
 *
 * @constant {WriteStream} resultsLogStream - The writable stream for logging results.
 */
const resultsLogStream = fs.createWriteStream(path.join(LOG_FOLDER, 'results.log'), { flags: 'a' });

/**
 * A writable stream for logging results to a file named 'results.log' located in the LOG_FOLDER directory.
 * The stream is opened in append mode, meaning new data will be added to the end of the file.
 *
 * @constant {WriteStream} resultsLogStream - The writable stream for logging results.
 */
const errorsLogStream = fs.createWriteStream(path.join(LOG_FOLDER, 'errors.log'), { flags: 'a' });

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
 * Recursively retrieves all files from a given directory.
 * 
 * @param {string} dir - The directory to search for files.
 * @param {string[]} [fileList=[]] - An array to accumulate the file paths.
 * @returns {string[]} An array of file paths.
 */
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

/**
 * Processes a single pricing file, retrieves analytics data, and updates the progress bar.
 * 
 * @param {string} filePath - The path to the pricing file.
 * @param {cliProgress.SingleBar} progressBar - The progress bar to update.
 * @param {Record<string, any>} analyticsData - The object to store analytics data.
 * @returns {Promise<void>} A promise that resolves when the file processing is complete.
 */
async function processFile(filePath: string, progressBar: cliProgress.SingleBar, analyticsData: Record<string, any>): Promise<void> {
    try {
        const pricing: Pricing = retrievePricingFromPath(filePath);
        const pricingService = new PricingService(pricing);
        const analytics = await pricingService.getAnalytics();

        const saasName = pricing.saasName;
        const createdAt = pricing.createdAt;

        if (!analyticsData[saasName]) {
            analyticsData[saasName] = {};
        }

        const dateKey = createdAt.toISOString().split('T')[0];
        analyticsData[saasName][dateKey] = analytics;
    } catch (error) {
        errorsLogStream.write(`Error processing file ${filePath}: ${(error as Error).message}\n\n`);
    } finally {
        progressBar.increment();
    }
}

/**
 * Main function that orchestrates the extraction and processing of pricing analytics.
 * 
 * - Retrieves all pricing files from the data directory.
 * - Initializes and starts a progress bar.
 * - Processes each file to extract analytics data.
 * - Writes the results and errors to log files.
 * 
 * @returns {Promise<void>} A promise that resolves when the main process is complete.
 */
async function main(): Promise<void> {
    const files = getAllFiles(DATA_DIR);
    const progressBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    progressBar.start(files.length, 0);

    const analyticsData: Record<string, any> = {};

    await Promise.all(files.map(file => processFile(file, progressBar, analyticsData)));

    progressBar.stop();

    const sortedSaasNames = Object.keys(analyticsData).sort();
    for (const saasName of sortedSaasNames) {
        resultsLogStream.write(`\t\t--------- ${saasName} ---------\n`);
        const years = Object.keys(analyticsData[saasName]).sort();
        years.forEach(year => {
            resultsLogStream.write(`\t\t------ ${year} ------\n`);
            resultsLogStream.write(`${JSON.stringify(analyticsData[saasName][year], null, 2)}\n`);
        });
        resultsLogStream.write('\n');
    }

    resultsLogStream.end();
    errorsLogStream.end();
}

main();