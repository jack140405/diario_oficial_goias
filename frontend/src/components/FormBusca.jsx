import React, { useState } from 'react';
import axios from 'axios';

export default function FormBusca() {
  const [palavra, setPalavra] = useState('');
  const [quantidade, setQuantidade] = useState(5);
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus('Processando...');

    try {
      const res = await axios.post(
        'http://127.0.0.1:5000/buscar',
        { palavra, quantidade, email },
        { timeout: 120000 }
      );

      setStatus('Concluído: ' + JSON.stringify(res.data));
    } catch (err) {
      setStatus('Erro: ' + (err.response?.data?.erro || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="form">
      <input
        placeholder="Palavra-chave"
        value={palavra}
        onChange={(e) => setPalavra(e.target.value)}
        required
      />

      <input
        type="number"
        min="1"
        value={quantidade}
        onChange={(e) => setQuantidade(e.target.value)}
      />

      <input
        type="email"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <button type="submit" disabled={loading}>
        {loading ? 'Processando...' : 'Buscar e Enviar'}
      </button>

      <div className="status">{status}</div>
    </form>
  );
}
