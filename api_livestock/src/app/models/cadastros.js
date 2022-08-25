import mongoose from "../../database";

const CadastroSchema = new mongoose.Schema(
  {
    nome: {
      type: String,
      required: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },
    ativo: {
      type: Boolean,
      default: false,
    },
    confirmacaoCadastro: {
      token: {
        type: String,
        required: false,
      },
      dataExpiracao: {
        type: Date,
        required: false,
      },
    },
  },
  { timestamps: true }
);

const Cadastro = mongoose.model("Cadastro", CadastroSchema, "cadastros");

module.exports = Cadastro;
