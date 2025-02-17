[![CC BY 4.0][cc-by-shield]][cc-by]

# 📊 Taming Complexity: Automated Analysis of Intelligent Pricings - Supplementary Material

This repository contains the laboratory package for the paper **Taming Complexity: Automated Analysis of Intelligent Pricings**, which includes scripts and MiniZinc models to replicate the validation performed in the study. Driven by the paper's main contribution, the primary goal of this package is to leverage the proposed automated analysis formalization and operations, among others, to uncover latent information in SaaS pricing models.

## 📚 Table of Contents

1. [⚙️ Prerequisites](#️-prerequisites)
2. [🚀 How to Replicate the Experiment](#-how-to-replicate-the-experiment)
3. [📂 Further Explanation About the Package](#-further-explanation-about-the-package)
   - [🔍 Project's Structure](#-projects-structure)
   - [📜 Scripts](#-scripts)
   - [📦 Dependencies](#-dependencies)
4. [📜 License](#-license)
5. [⚠️ Disclaimer](#️-disclaimer)

## ⚙️ Prerequisites

To run this package, ensure you have the following:

- **Node.js**: Version 20.x or higher
- **NPM**: Version 10.x or higher


## 🚀 How to Replicate the Experiment

To replicate the experiment, follow these simple steps:

1. **Clone the repository and checkout to the CAISE'25-Research-Track tag**:

```bash
git clone https://github.com/isa-group/SaaS-analysis.git
cd saas-analysis
git checkout CAISE\'25-Research-Track
```

2. **Install the dependencies**:

```bash
npm install
```

3. **Run the experiment**:

```bash
npm run experiment
```

### What Happens During the Experiment?

When executing `npm run experiment`, the following steps are performed:

1.	**Adding versioning information** to the pricing models if they don’t already have it.
2.	**Generating .dzn files** for the MiniZinc models from the Pricing2Yaml specifications. These files are primarily to showcase the results of the mapping from each Pricing2Yaml specification to a DZN file. However, they are not used during the experiment.
3.	**Extracting analytics** from the pricings of the real-world dataset (*data/pricings/yaml/real-v2*), generating:

    - A **JSON file** with the extracted analytics in **data/pricings/json/** (the file will be titled: `analytics-{timestamp}.json`).
    - Detailed **logs** of results and errors in the **logs/** directory (in the folder: `pricing-analyitic-{timestamp}`).

4.	**Validation** of the pricings included within the synthetic dataset (*data/pricings/yaml/synthetic*), generating:

    - Summary and detailed **logs** of results in the **logs/** directory (in the folder: `validation-{timestamp}`).

::: warning
Don't worry about the errors that are logged during the generation of the .dzn files. These errors are expected since most of inconsistencies from the synthetic dataset are detected by the Pricing4TS parser.
:::

### Are you using VSCode?

We have configured some launch configurations to ease the launch of the experiments independently 😄.

## 📂 Further Explanation About the Package

### 🔍 Project’s Structure

```bash
saas-analysis
├── .vscode
├── data
│   ├── models
│   │   └── minizinc # Models utilized by Pricing4TS to get some analytics
│   │       ├── operations
│   │       │   ├── analysis
│   │       │   │   ├── cheapest-subscription.mzn
│   │       │   │   ├── configuration-space.mzn
│   │       │   │   └── most-expensive-subscription.mzn
│   │       │   ├── filter
│   │       │   │   ├── cheapest-filtered-subscription.mzn
│   │       │   │   ├── filter.mzn
│   │       │   │   ├── filtered-configuration-space.mzn
│   │       │   │   └── most-expensive-filtered-subscription.mzn
│   │       │   ├── validation
│   │       │   │   ├── valid-pricing.mzn
│   │       │   │   └── valid-subscription.mzn
│   │       └── PricingModel.mzn
│   └── pricings
│       ├── dzn           # Generated after running the experiment
│       │   └── ...
│       ├── json          # Generated after running the experiment
│       │   └── ...
│       └── yaml
│           ├── real      # Pricing2Yaml files from the real-world dataset
│           │   └── ...
│           └── synthetic # Pricing2Yaml files from the synthetic dataset
│               └── ...
├── logs                  # Generated after running the experiment
├── node_modules          # Generated after running npm install
├── src
│   ├── scripts
│   │   ├── analytics
│   │   │   ├── extract-analytics-from-file.ts
│   │   │   └── extract-analytics.ts        
│   │   ├── utils
│   │   │   ├── extract-analytics-from-file.ts
│   │   │   └── extract-analytics.ts        
│   │   └── validation
│   │       ├── synthetic-dataset-experiment.ts
│   │       └── synthetic-pricing-validation.ts        
│   └── services
│       └── logging.service.ts
├── .gitignore
├── LICENSE
├── package-lock.json
├── package.json
├── README.md
└── tsconfig.json
```

### 📜 Scripts

The package includes the following scripts:

| Script Name            | Description                                                   | Usage Command                       |
|------------------------|---------------------------------------------------------------|-------------------------------------|
| **Extract Analytics¹** | Extracts analytics for all SaaS pricings in the dataset.      | `npm run analytics`                 |
| **File-Based Analytics¹** | Processes analytics from a specific file.                   | `npm run analytics-from-file <path-to-pricing-file>` |
| **Dataset Validation¹** | Runs the `valid subscription` operation over the whole synthetic dataset      | `npm run validation`                 |
| **File-Based Validation¹** | Validates a specific Pricing2Yaml file.                   | `npm run validation-from-file <path-to-pricing-file>` |
| **Add Versions**       | Adds missing versioning information to pricing models.        | `npm run add-versions-to-pricings`  |
| **Generate DZN Files** | Converts pricing models into `.dzn` files for MiniZinc.       | `npm run generate-dzn-files`        |
| **Analytics Experiment Workflow**| Executes the full pipeline of the analytics experiment.                | `npm run experiment:analytics`                |
| **Validation Experiment Workflow**| Executes the full pipeline of the validation experiment.                | `npm run experiment:validation`                |
| **Experiment Workflow**| Executes the full pipeline of the experiment, including analytics extraction and validation.                | `npm run experiment`                |

¹**Extract Analytics**, **File-Based Analytics**, **Dataset Validation** and **File-Based Validation** scripts leverages the [PricingService](https://github.com/Alex-GF/Pricing4TS/blob/v0.4.1/src/server/services/pricing.service.ts) from our library [Pricing4TS](https://github.com/Alex-GF/Pricing4TS). This library, developed as part of our Pricing-driven Development and Operation research initiatives, was specifically extended with the automated analysis formalization and operations presented in the paper.

The script utilizes the `getAnalytics(pricing: Pricing)` method from the service to process all pricing files located in the *data/pricings/yaml/real-v2* or *data/pricings/yaml/synthetic* directories, depending on the executed experiment. In the first case, the analytics extraction method is applied to each file, generating a JSON file with the extracted analytics in *data/pricings/json/* and detailed logs of results and errors in the *logs/* directory. In the second case, the validation method is applied to each file, generating summary and detailed logs of results in the *logs/* directory.

### 📦 Dependencies

**Production Dependencies**

- **cli-progress**: For progress visualization.
- **@types/cli-progress**: Type definitions for cli-progress.
- [**Pricing4TS**](https://github.com/Alex-GF/Pricing4TS): Our library for pricing-driven development and operations.

**Development Dependencies**

- **typescript**: Enables TypeScript support.
- **jest & ts-jest**: For testing.
- **ts-node**: To run TypeScript files directly.

## ⚠️ Disclaimer

This project is part of the research activities of the [ISA Group](https://www.isa.us.es/3.0/) and was specifically created as a laborratory package for the paper: "Taming Complexity: Automated Analysis of Intelligent Pricings". Please note that the project should be used with caution. We are not responsible for any damage caused by the use of this software. If you find any bugs or have any suggestions, please let us know by opening an issue in the [GitHub repository](https://github.com/isa-group/SaaS-analysis/issues) with the label: **CAISE'25-Research-Track**.

## 📜 License

This work is licensed under a [Creative Commons Attribution 4.0 International License] [cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg