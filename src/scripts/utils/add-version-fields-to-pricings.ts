import fs from "fs";
import path from "path";
import { logExperimentHeader } from "../../services/logging.service";

const VERSION_FIELD = "version:";
const VERSION_FIELD_VALUE = "version: '1.0'";

// Define the directory path where the YAML files are located
const directoryPath = path.join(__dirname, "../../../data/pricings/yaml/real-v2/");

function addVersionFieldToPricings(directoryPath: string) {
  const files = fs.readdirSync(directoryPath);

  for (const file of files) {
    const filePath = path.join(directoryPath, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      // Si es un directorio, llama a la función recursivamente
      addVersionFieldToPricings(filePath);
    } else if (filePath.endsWith(".yml")) {
      const content = fs.readFileSync(filePath, "utf8");
      if (!content.includes(VERSION_FIELD)) {
        const lines = content.split("\n");
        lines.splice(1, 0, VERSION_FIELD_VALUE);
        const updatedContent = lines.join("\n");
        fs.writeFileSync(filePath, updatedContent, "utf8");
      }
    }
  }
}

logExperimentHeader();

console.log(`Adding version field (if missing) to pricings in dataset...`);
addVersionFieldToPricings(directoryPath);
console.log('Done!\n');
