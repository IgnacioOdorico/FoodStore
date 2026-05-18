import { useState, type ChangeEvent, type SyntheticEvent } from "react";
import { useAuthStore } from "../../../store/useAuthStore";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
  const [formValues, setFormValues] = useState({ email: "", password: "" });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMessage(null);

    const user = await login(formValues.email, formValues.password).catch(() => null);
    if (!user) {
      setErrorMessage("Credenciales inválidas");
      return;
    }
    if (user.role === "admin" || user.role === "employee") {
      navigate("/dashboard");
    } else if (user.role === "client") {
      navigate("/orders");
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormValues((currentValues) => ({
      ...currentValues,
      [e.target.id === "login-email" ? "email" : "password"]: e.target.value,
    }));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        id="login-email"
        value={formValues.email}
        onChange={handleChange}
        type="text"
        placeholder="Ingresa tu email"
      />
      <input
        id="login-password"
        value={formValues.password}
        onChange={handleChange}
        type="password"
        placeholder="Ingresa tu contraseña"
      />
      <button type="submit">Entrar</button>

      {errorMessage && <p>{errorMessage}</p>}

      {/* CREDENCIALES REALES DEL SEED */}
      <ul>
        <li>admin@nachopizza.com / Admin1234! → admin</li>
        <li>juan@ejemplo.com / Juan1234! → client</li>
      </ul>
    </form>
  );
};
