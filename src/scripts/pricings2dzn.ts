import fs from "fs";
import path from "path";
import { saveDZNfile } from "pricing4ts";

// Define the directory path where the YAML files are located
const directoryPath = path.join(__dirname, "../../data/pricings/yaml/");

function readYamlFiles(directoryPath: string) {
  const files = fs.readdirSync(directoryPath);
  for (const file of files) {
    const filePath = path.join(directoryPath, file);
    const pathYear = /(\d{4})/.exec(filePath)?.[0];
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      // Si es un directorio, llama a la función recursivamente
      readYamlFiles(filePath);
    } else if (filePath.endsWith(".yml")) {
      saveDZNfile(filePath, `data/pricings/dzn/${pathYear}`);
    }
  }
}

readYamlFiles(directoryPath);
