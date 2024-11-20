import fs from "fs";
import path from "path";
import { saveDZNfile } from "pricing4ts";

// Define the directory path where the YAML files are located
const directoryPath = path.join(__dirname, "../../data/pricings/yaml/real/");

function readYamlFiles(directoryPath: string) {
  
  let numberOfParsedFiles = 0;
  
  const files = fs.readdirSync(directoryPath);
  for (const file of files) {
    const filePath = path.join(directoryPath, file);
    const pathYear = path.basename(path.dirname(filePath));
    const pathType = path.basename(path.dirname(path.dirname(filePath)));
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      // Si es un directorio, llama a la función recursivamente
      numberOfParsedFiles = numberOfParsedFiles + readYamlFiles(filePath);
    } else if (filePath.endsWith(".yml")) {
      const fileName = path.basename(filePath, ".yml");
      const outputFilePath = path.join(__dirname, `../../data/pricings/dzn/${pathType}/${pathYear}/${fileName}.dzn`);
      
      if (fs.existsSync(outputFilePath)) {
        numberOfParsedFiles = numberOfParsedFiles + 1;
        continue;
      }
    
      saveDZNfile(filePath, `data/pricings/dzn/${pathYear}`);
      numberOfParsedFiles = numberOfParsedFiles + 1;
    }
  }

  return numberOfParsedFiles;
}

console.log(`Reading YAML files and parsing to MiniZinc datafiles...`);
const datasetSize = readYamlFiles(directoryPath);
console.log(`Done! Size of the dataset: ${datasetSize} pricings\n`);
