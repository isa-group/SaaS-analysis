# SaaS Analysis

The aim of this repository is to centralize the work performed by the ISA Group to write the paper for ICSOC 2024 about the current status of SaaS pricings.

## Work Status

The cells of the following table should be filled as follows in order to keep track of the work status:

- ✅: The SaaS is modeled for the indicated year.
- 🔄: The SaaS is being modeled for the indicated year.
- ✖️: There is a snapshot, but a clear feature list cannot be extracted.
- ❌: There isn't a snapshot for the SaaS in the indicated year.

Empty cells indicate that the SaaS has not been modeled yet.

| SaaS          | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| ------------- | :--: | :--: | :--: | :--: | :--: | :--: |
| ClickUp       |  ✖️   |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Microsoft 365 |  🔄  |  🔄  |  🔄  |  🔄  |  🔄  |  🔄  |
| Salesforce    |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Slack         |  ✅  |  ✅  |  ❌  |  ❌  |  ✅  |  ✅  |
| Buffer        |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Hypercontext  |  ❌  |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |
| DocuSign      |  ❌  |  ❌  |  ❌  |  ❌  |      |      |
| OpenPhone     |  ❌  |  ❌  |  ❌  |  ✅  |  ✅  |  ✅  |
| Pumble        |  ❌  |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |
| Tableau       |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Quip          |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| MailChimp     |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Deskera       |  ❌  |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |
| UserGuiding   |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Crowdcast     |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Planable      |  ✖️  |  ✖️  |  ✖️  |  ✅   |  🔄  |  🔄  |
| Databox       |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Trustmary     |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Evernote      |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Canva         |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Clockify      |  ❌  |  ❌  |  ❌  |  ✅  |  ✅  |  ✅  |
| GitHub        |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Figma         |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Jira          |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Dropbox       |  ✖️  |  ✖️  |  ✅  |  ✅  |  ✅  |  ✅  |
| Overleaf      |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Postman       |  ❌  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Zapier        |  ✅  |  ✅  |  ❌  |  ✅  |  ✅  |  ✅  |
| Box           |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |
| Wrike         |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  |

## Research Questions

The following research questions are being considered for the paper:

### ¿Cómo han evolucionado los pricings?

1. ¿Cómo ha evolucionado el número de planes de precios ofrecidos por los SaaS a lo largo del tiempo? | ¿Han crecido en media? ¿hay muchos o pocos casos que rompan la tendencia general?

2. ¿Cómo ha evolucionado el número de features ofrecidas por los SaaS a lo largo del tiempo? | ¿Han crecido en media? ¿hay muchos o pocos casos que rompan la tendencia general? (Se puede estudiar completa o por plan)

### Sobre el estado actual

1. ¿Qué frecuencia hay de aparición de los addOns en los pricings actuales? | ¿Es común que existan addOns en los planes de precios hoy en día?

2. ¿Cómo se distribuyen los "saltos monetarios" entre los distintos planes de precios? | Si calculamos la relación entre dos planes consecutivos, ¿existe una relación que se cumple?

### Alternativas a recuperar del estudio original

1. How princings are evolving in terms of number of features?

2. Although the plan-based pricing structure is the most widely used nowadays, are plan-based pricings incorporating add-ons?

3. What is the relationship between the evolution of add-ons and plans?

## Important Links

- 37 Popular SaaS: https://clickup.com/blog/saas-examples/

## Scripts

### Install Dependencies

Dependencies can be installed using the following command: 

```bash
pip install -r requirements.txt
```

### Generate Yaml4SaaS

> info: You need to use Python 3.9 or higher to run the script.

The script generator.py can be used to generate the yaml file for a SaaS in a given year. The script can be executed as follows:

```bash
cd scripts
python generator.py --saas_name Slack --year 2022 --html_url https://web.archive.org/web/20201022160503/https://slack.com/intl/es-es/pricing --previous_html_url https://web.archive.org/web/20191031074849/https://slack.com/intl/es-es/pricing --year-gap 1
```

It receives the following arguments:
- `--saas_name`: Name of the SaaS to be analyzed.
- `--year`: Year to be analyzed.
- `--html_url`: URL of the HTML to be analyzed. It should be a URL from the Wayback Machine.
- `--previous_html_url`: URL of the previous HTML to be analyzed. It should be a URL from the Wayback Machine.
- `--year_gap`: Number of years between the current year and the previous year. Default is 1. If the year gap is less than 1, the previous year will be a future year.

The script will generate a yaml file in the `pricings` folder with the information of the SaaS in the given year subfolder. For executing the script, an environment variable `GOOGLE_AI_STUDIO` should be set with the API key of the Google AI Studio API. This API key enables the script to use gemini-1.5-flash or gemini-1.5-pro models for the yaml generation. These models are multimodal models that use both text and images to generate the yaml file. For using these models with the free tier of the Google AI Studio API, the script should be executed in a region that supports it (it may be neccesary to use a VPN). The environment variable can be set using a `.env` file in the `scripts` folder of the repository with the following content:

```bash
GOOGLE_AI_STUDIO=YOUR_API_KEY
```

Finally, a log file will be generated in the `logs` folder (inside the `scripts` folder) with the name `generator.log` that will contain the information of the execution of the script.