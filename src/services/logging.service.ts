export function logExperimentHeader(){
    const experimentName = "Pricings Validation";
    const articleTitle = "Automated Analysis of iPricing";
    const authors = "A. García-Fernández, J.A. Parejo, P. Trinidad, and A. Ruiz-Cortés";
    const labPack = "1.0";
    const date = new Date().toISOString().split("T")[0]; // Formato YYYY-MM-DD

    console.log(`
    ============================================
                EXPERIMENT INITIALIZATION: ${experimentName}
    ============================================
    Article: "${articleTitle}"
    Authors: ${authors}
    LabPack: ${labPack}
    Date: ${date}
    ============================================
    `);
}