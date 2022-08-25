import mongoose from "../../database";

const ProdLeiteSchema = new mongoose.Schema(
  {
    brinco: {
      type: String,
      require: true,
    },
    ordenha1: {
      type: Number,
      require: false,
    },
    ordenha2: {
      type: Number,
      require: true,
    },
    ordenha3: {
      type: Number,
      require: true,
    },
    prodTotal: {
      type: Number,
      require: true,
    },
    date: {
      type: String,
      require: false,
    },
  },
  { timestamps: true }
);

const ProdLeite = mongoose.model("ProdLeite", ProdLeiteSchema, "prodLeite");

module.exports = ProdLeite;
