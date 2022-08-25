import mongoose from "../../database";

const ProdLeiteGeralSchema = new mongoose.Schema(
  {
    date: {
      type: String,
      require: false,
    },
    animais: {
      type: Number,
      require: false,
    },
    producao: {
      type: Number,
      require: false,
    },
    lote: {
      type: String,
      require: false,
    },
  },
  { timestamps: true }
);

const ProdLeiteGeral = mongoose.model(
  "ProdLeiteGeral",
  ProdLeiteGeralSchema,
  "prodLeiteGeral"
);

module.exports = ProdLeiteGeral;
