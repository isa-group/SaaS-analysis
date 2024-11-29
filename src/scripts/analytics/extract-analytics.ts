/**
 * ------------ Overview ------------
 * This script processes multiple Pricing2Yaml files to extract analytics and logs the results.
 *
 * The script recursively scans the specified data directory (../data/pricings/yaml/real/) for pricing files, processes each file
 * using the `pricing4ts` library, and generates analytics for each SaaS pricing. The results
 * and any errors encountered during the process are logged into separate files in a timestamped
 * directory within the `logs` folder.
 *
 * ------------ Features ------------
 * - Recursively scans the `../data/pricings/yaml/real/` directory to find all pricing files.
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

import * as fs from "fs";
import * as path from "path";
import { Pricing, retrievePricingFromPath } from "pricing4ts";
import { PricingService } from "pricing4ts/server";
import cliProgress from "cli-progress";

/**
 * The directory path where pricing YAML files are stored.
 * This constant is used to specify the location of the data files
 * that will be processed by the analytics extraction script.
 * @constant {string}
 */
const DATA_DIR = "data/pricings/yaml/real";

/**
 * Directory where log files are stored.
 *
 * @constant {string}
 */
const LOG_DIR = "logs";

/**
 * File where the JSON file with the anaylitics data will be stored.
 *
 * @constant {string}
 */
const JSON_DIR = "data/pricings/json";

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
 * A writable stream for logging the summary of results to a file named 'summary.log' located in the LOG_FOLDER directory.
 * The stream is opened in append mode, meaning new data will be added to the end of the file.
 *
 * @constant {WriteStream} summaryLogStream - The writable stream for logging the summary of the results.
 */
const summaryLogStream = fs.createWriteStream(
  path.join(LOG_FOLDER, "summary.log"),
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
 * Create the JSON_DIR directory if it does not exist.
 */
if (!fs.existsSync(JSON_DIR)) {
  fs.mkdirSync(JSON_DIR);
}

/**
 * The total number of pricing files found in the data directory.
 */
let numberOfFiles = 0;

/**
 * Recursively retrieves all files from a given directory.
 *
 * @param {string} dir - The directory to search for files.
 * @param {string[]} [fileList=[]] - An array to accumulate the file paths.
 * @returns {string[]} An array of file paths.
 */
function getAllFiles(dir: string, fileList: string[] = []): string[] {
  const files = fs.readdirSync(dir);
  files.forEach((file) => {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      getAllFiles(filePath, fileList);
    } else {
      numberOfFiles++;
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
async function processFile(
  filePath: string,
  progressBar: cliProgress.SingleBar,
  analyticsData: Record<string, any>
): Promise<void> {
  try {
    const startTime = Date.now();
    const pricing: Pricing = retrievePricingFromPath(filePath);
    const pricingService = new PricingService(pricing);
    const analytics = await pricingService.getAnalytics();

    const saasName = _formatSaaSName(pricing.saasName);
    const createdAt = pricing.createdAt;

    if (!analyticsData[saasName]) {
      analyticsData[saasName] = {};
    }

    const dateKey = createdAt.toISOString().split("T")[0];
    const executionTime = Date.now() - startTime;

    if (!analyticsData[saasName][dateKey]) {
      analyticsData[saasName][dateKey] = {};
      analyticsData[saasName][dateKey].analytics = analytics.configurationSpaceSize;
      analyticsData[saasName][dateKey].yaml_path = filePath;
      analyticsData[saasName][dateKey].executionTime = executionTime;
    }
  } catch (error) {
    errorsLogStream.write(
      `Error processing file ${filePath}: ${(error as Error).message}\n\n`
    );
  } finally {
    progressBar.increment();
  }
}

function generateJsonFileFromAnalytics(
  analyticsData: Record<string, any>
): void {
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const jsonFilePath = path.join(JSON_DIR, `analytics-${timestamp}.json`);

  // Process analyticsData to add yaml_path and format SaaS names
  for (const saasName in analyticsData) {
    const [_, ...rest] = saasName.split(" ");
    const formattedSaasName = _formatSaaSName(saasName);
    const product = rest.join(" ").replace(/^-/, "");

    analyticsData[formattedSaasName] = analyticsData[saasName];
    if (formattedSaasName !== saasName) {
      delete analyticsData[saasName];
    }

    for (const year in analyticsData[formattedSaasName]) {
      if (product) {
        analyticsData[formattedSaasName][year].product = product.trim();
      }
    }
  }

  for (const saasName in analyticsData) {
    const sortedYears = Object.keys(analyticsData[saasName]).sort(
      (a, b) => new Date(b).getTime() - new Date(a).getTime()
    );
    const sortedAnalytics: any = {};
    sortedYears.forEach((year) => {
      sortedAnalytics[year] = analyticsData[saasName][year];
    });
    analyticsData[saasName] = sortedAnalytics;
    analyticsData[saasName] = Object.keys(analyticsData[saasName]).map(
      (date) => ({
        ...analyticsData[saasName][date],
        date,
      })
    );
  }

  const jsonData = JSON.stringify(analyticsData, null, 2);
  fs.writeFileSync(jsonFilePath, jsonData);
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
  const progressBar = new cliProgress.SingleBar(
    {},
    cliProgress.Presets.shades_classic
  );
  progressBar.start(files.length, 0);

  const analyticsData: Record<string, any> = {};

  for (const file of files) {
    await processFile(file, progressBar, analyticsData);
  }

  progressBar.stop();

  // Build the results log

  resultsLogStream.write(
    `+---------------------+-----------+-----------+-----------+-----------+-----------+-----------+\n` +
    `| SaaS Name           | 2019      | 2020      | 2021      | 2022      | 2023      | 2024      |\n` +
    `+---------------------+-----------+-----------+-----------+-----------+-----------+-----------+\n`
  );

  const sortedSaasNames = Object.keys(analyticsData).sort();
  for (const saasName of sortedSaasNames) {
    const row = [saasName.padEnd(20)];
    const dates = Object.keys(analyticsData[saasName]).sort();

    const years = ['2019', '2020', '2021', '2022', '2023', '2024'];
    for (const year of years) {
      const dateEntry = dates.find(date => date.startsWith(year));
      const value = (dateEntry ? analyticsData[saasName][dateEntry]?.executionTime : 'N/A').toString();
      row.push(value.padEnd(8) + 'ms');
    }

    resultsLogStream.write(`| ${row.join('| ')}|\n`);
  }

  resultsLogStream.write(
    `+---------------------+-----------+-----------+-----------+-----------+-----------+-----------+\n`
  );
  
  // Build the summary log

  const executionTimes = Object.values(analyticsData).flatMap(saas =>
    Object.values(saas).map(entry => (entry as any).executionTime)
  );
  
  const numPricingsExtracted = Object.values(analyticsData).reduce(
    (acc, saas) => acc + Object.keys(saas).length,
    0
  );
  const avgExecutionTime = executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length;
  executionTimes.sort((a, b) => a - b);
  const q1 = executionTimes[Math.floor((executionTimes.length / 4))];
  const q3 = executionTimes[Math.ceil((executionTimes.length * (3 / 4))) - 1];
  const iqr = q3 - q1;
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;
  const filteredTimes = executionTimes.filter(time => time >= lowerBound && time <= upperBound);
  const avgExecutionTimeNoOutliers = filteredTimes.reduce((a, b) => a + b, 0) / filteredTimes.length;

  summaryLogStream.write(
    `+----------------------------------+-------------------------+\n` +
    `| Dataset Size                     | ${numberOfFiles.toString().padEnd(24)}|\n` +
    `| Pricings extracted               | ${numPricingsExtracted.toString().padEnd(24)}|\n` +
    `| Avg Execution Time               | ${avgExecutionTime.toFixed(2)} ms${''.padEnd(21-avgExecutionTime.toFixed(2).length)}|\n` +
    `| Avg Execution Time (No Outliers) | ${avgExecutionTimeNoOutliers.toFixed(2)} ms${''.padEnd(21-avgExecutionTimeNoOutliers.toFixed(2).length)}|\n` +
    `+----------------------------------+-------------------------+\n`
  );

  resultsLogStream.end();
  summaryLogStream.end();
  errorsLogStream.end();

  generateJsonFileFromAnalytics(analyticsData);
}

/**
 * Formats the SaaS name by capitalizing the first letter of the first word.
 *
 * @param {string} saasName - The original SaaS name.
 * @returns {string} The formatted SaaS name.
 */
function _formatSaaSName(saasName: string): string {
  const [firstWord] = saasName.split(" ");
  return firstWord.charAt(0).toUpperCase() + firstWord.slice(1).toLowerCase();
}

main();