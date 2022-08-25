import mongoose from "../../database";

const AlimentoSchema = new mongoose.Schema(
  {
    lote: {
      type: String,
      require: true,
    },
    date: {
      type: String,
      require: false,
    },
    totalLote: {
      type: Number,
      require: true,
    },
    mediaVaca: {
      type: Number,
      require: true,
    },
    numAnimais: {
      type: Number,
      require: false,
    },
    alimento: {
      type: String,
      require: false,
    },
  },
  { timestamps: true }
);

const Alimento = mongoose.model("Alimento", AlimentoSchema, "alimento");

module.exports = Alimento;
