# CAISE'25: Laboratory Package

This repository contains the laboratory package of the paper CAISE’25, which includes the necessary scripts and minizinc models to replicate the validation performed in the paper. Thus, the main objective of this package is to apply the automated analyisis techniques, among others, to uncover latent information within pricings.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [How to replicate the experiment](#how-to-replicate-the-experiment)
3. [Further Explanation About the Package](#further-explanation-about-the-package)
   - [Project's Structure](#projects-structure)
   - [Scripts](#scripts)
   - [Dependencies](#dependencies)
4. [License](#license)
5. [Disclaimer](#disclaimer)

## Prerrequisites
<a href="#prerequisites"></a>

- Node.js (20.x or higher)
- NPM (10.x or higher)

## How to replicate the experiment?

To run the experiment in order to replicate it, you just need to follow three simple steps:

1. Clone the repository and checkout to the CAISE'25 tag:

```bash
git clone https://github.com/isa-group/SaaS-analysis.git
cd saas-analysis
git checkout dataset/dzn
```

2. Install the dependencies:

```bash
npm install
```

3. Run the experiment:

```bash
npm run experiment
```

This command will execute the full pipeline of the experiment, which includes:

1. **Adding versioning information to the pricings**, if they don't have it.
2. **Generating the .dzn files for the MiniZinc models form the Pricing2Yaml specifications of the pricings in the dataset.** However, this files are not used during the analysis, since they are computed on-the-fly, but they are generated for the sake of reproducibility and debugging.
3. **Extracting the analytics from the pricings in the dataset.** This will process each pricing file in YAML format located in the data/pricings/yaml/real directory and, as a result, it will generate multiple outputs, including: 

    - A JSON file in `data/pricings/json/` with the extracted analytics

    - Detailed logs of results and encountered errors in the `logs` directory.

## Further explanation about the package

### Project's Structure

```bash
saas-analysis
├── .vscode
├── data
│   └── pricings
│       ├── dzn          # Appears after the experiment is replicated
│       │   └── ...
│       ├── json          # Appears after the experiment is replicated
│       │   └── ...
│       └── yaml
│           └── real
│               └── ...
├── logs                  # Appears after the experiment is replicated
├── node_modules          # Appears after the experiment is replicated
├── src
│   ├── scripts
│   │   ├── add-version-fields-to-pricings.ts
│   │   ├── extract-analytics-from-file.ts
│   │   ├── extract-analytics.ts
│   │   └── pricings2dzn.ts
│   └── services
│       └── logging.service.ts
├── .gitignore
├── LICENSE
├── package-lock.json
├── package.json
├── README.md
└── tsconfig.json
```

### Scripts

The package includes the following scripts:

| Script Name            | Description                                                   | Usage Command                       |
|------------------------|---------------------------------------------------------------|-------------------------------------|
| **Extract Analytics¹**  | Extracts analytics for all SaaS pricings within the dataset in `data/pricings/yaml/real`.                   | `npm run analytics`                 |
| **File-Based Analytics** | Processes analytics from a specific file.                   | `npm run analytics-from-file <path-to-pricing-file>`       |
| **Add Versions**       | Updates Pricing2Yaml specifications that lack a version fieldwith version-specific fields.         | `npm run add-versions-to-pricings`  |
| **Generate DZN Files** | Converts pricing models into `.dzn` files for MiniZinc.      | `npm run generate-dzn-files`        |
| **Experiment Workflow**| Executes the full pipeline: adding versions, generating `.dzn` files and analytics extraction. | `npm run experiment` |

¹The **Extract Analytics** script leverages the [PricingService](https://github.com/Alex-GF/Pricing4TS/blob/v0.3.1/src/services/pricing.service.ts) from our library [Pricing4TS](https://github.com/Alex-GF/Pricing4TS). This library, developed as part of our Pricing-driven Development and Operation research initiatives, was specifically extended with the automated analysis formalization and operations presented in the paper.

By leveraging this service, more specifically its method `getAnalytics(pricing: Pricing)`, the script processes all pricing files located in the *data/pricings/yaml/real* directory, applies the analytics extraction method to each file and generates the outputs described earlier: a JSON file containing the extracted analytics (*data/pricings/json/*) and detailed logs of results and errors (*logs/*).

### Dependencies

- cli-progress: For progress visualization.
- @types/cli-progress: Type definitions for cli-progress.

### Development Dependencies

- typescript: For TypeScript support.
- jest & ts-jest: For testing.
- ts-node: To run TypeScript directly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is part of the research activities of the [ISA Group](https://www.isa.us.es/3.0/) and was specifically created as a laborratory package for the paper: CAISE'25. Please note that the project should be used with caution. We are not responsible for any damage caused by the use of this software. If you find any bugs or have any suggestions, please let us know by opening an issue in the [GitHub repository](https://github.com/isa-group/SaaS-analysis/issues) with the label: **CAISE'25**.