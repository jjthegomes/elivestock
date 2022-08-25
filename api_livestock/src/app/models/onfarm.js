import mongoose from "../../database";

//Fazenda	BarCode	Lado	Brinco	OBS	Data	Tipo	Quarto	Grau	Resultado	Gram Pos	Gram Neg	E coli	Enterococcus spp	Klebsiella / Enterobacter	Lactococcus spp	Outros Gram-neg	Outros Gram-pos	Prototheca / Levedura	Pseudomonas spp	Serratia spp	Staph não aureus	Staph aureus	Strep agalactiae / dysgalactiae	Strep uberis

const OnfarmSchema = new mongoose.Schema(
  {
    fazenda: {
      type: String,
      require: false,
    },
    barcode: {
      type: String,
      require: false,
    },
    brinco: {
      type: String,
      require: false,
    },
    lado: {
      type: String,
      require: false,
    },
    data: {
      type: String,
      require: false,
    },
    tipo: {
      type: String,
      require: false,
    },
    obs: {
      type: String,
      require: false,
    },
    quarto: {
      type: String,
      require: false,
    },
    grau: {
      type: String,
      require: false,
    },
    resultado: {
      type: String,
      require: false,
    },
    gramPositiva: {
      type: String,
      require: false,
    },
    gramNegativa: {
      type: String,
      require: false,
    },
    ecoli: {
      type: String,
      require: false,
    },
    enterococcusSpp: {
      type: String,
      require: false,
    },
    klebsiellaEnterobacter: {
      type: String,
      require: false,
    },
    lactococcusSpp: {
      type: String,
      require: false,
    },
    outrosGramNegativa: {
      type: String,
      require: false,
    },
    outrosGramPositiva: {
      type: String,
      require: false,
    },
    AtbInjetavel: {
      type: String,
      require: false,
    },
    protothecaLevedura: {
      type: String,
      require: false,
    },
    pseudomonasSpp: {
      type: String,
      require: false,
    },
    serratiaSpp: {
      type: String,
      require: false,
    },
    staphNãoAureus: {
      type: String,
      require: false,
    },
    staphAureus: {
      type: String,
      require: false,
    },
    strepAgalactiaeDysgalactiae: {
      type: String,
      require: false,
    },
    strepUberis: {
      type: String,
      require: false,
    },
  },
  { timestamps: true }
);

const Onfarm = mongoose.model("Onfarm", OnfarmSchema, "onfarm");

module.exports = Onfarm;
