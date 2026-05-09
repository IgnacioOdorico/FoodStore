import { useState, type ChangeEvent, type SyntheticEvent } from "react";
import { useAuthStore } from "../../../store/useAuthStore";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
  const [formValues, setFormValues] = useState("");
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = (e: SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const user = login(formValues);
    if (!user) {
      console.log("Usuario no encontrado");
      return;
    }
    if (user.role === "admin" || user.role === "employee") {
      navigate("/dashboard");
    } else if (user.role === "client") {
      navigate("/orders");
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormValues(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        id="login-email"
        value={formValues}
        onChange={handleChange}
        type="text"
        placeholder="Ingresa tu email"
      />
      <button type="submit">Entrar</button>

      {/* MOCK USERS */}
      <ul>
        <li>admin@app.com → admin</li>
        <li>emp@app.com → employee</li>
        <li>client@app.com → client</li>
      </ul>
    </form>
  );
};
