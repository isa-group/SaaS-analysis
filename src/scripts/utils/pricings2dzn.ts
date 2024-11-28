import fs from "fs";
import path from "path";
import { saveDZNfile } from "pricing4ts/server";

// Define the directory path where the YAML files are located
const directoryPath = path.join(__dirname, "../../../data/pricings/yaml/");

function readYamlFiles(directoryPath: string) {
  
  let numberOfParsedFiles = 0;
  
  const files = fs.readdirSync(directoryPath);
  for (const file of files) {
    const filePath = path.join(directoryPath, file);
    const pathName = path.basename(path.dirname(filePath));
    const pathTypeForRealWorld = path.basename(path.dirname(path.dirname(filePath)));
    const pathTypeForSynthetic = path.basename(path.dirname(path.dirname(path.dirname(filePath))));
    const isSynthetic = pathTypeForSynthetic === "synthetic";
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      // Si es un directorio, llama a la función recursivamente
      numberOfParsedFiles = numberOfParsedFiles + readYamlFiles(filePath);
    } else if (filePath.endsWith(".yml")) {
      const fileName = path.basename(filePath, ".yml");
      const outputFilePath = path.join(__dirname, isSynthetic ? `../../data/pricings/dzn/${pathTypeForSynthetic}/${pathTypeForRealWorld}/${pathName}/${fileName}.dzn` : `../../data/pricings/dzn/${pathTypeForRealWorld}/${pathName}/${fileName}.dzn`);
      
      if (fs.existsSync(outputFilePath)) {
        numberOfParsedFiles = numberOfParsedFiles + 1;
        continue;
      }
    
      saveDZNfile(filePath, isSynthetic ? `data/pricings/dzn/${pathTypeForSynthetic}/${pathTypeForRealWorld}/${pathName}/${fileName}.dzn` : `data/pricings/dzn/${pathTypeForRealWorld}/${pathName}/${fileName}.dzn`);
      numberOfParsedFiles = numberOfParsedFiles + 1;
    }
  }

  return numberOfParsedFiles;
}

console.log(`Reading YAML files and parsing to MiniZinc datafiles...`);
const datasetSize = readYamlFiles(directoryPath);
console.log(`Done! Size of the dataset: ${datasetSize} pricings\n`);
