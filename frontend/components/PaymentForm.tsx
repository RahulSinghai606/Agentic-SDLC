import React, { useState } from 'react';
import axios from 'axios';

const PaymentForm: React.FC = () => {
  const [amount, setAmount] = useState(0);
  const [currency, setCurrency] = useState('usd');
  const [clientSecret, setClientSecret] = useState('');
  const [message, setMessage] = useState('');

  const handleCreatePaymentIntent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/create-payment-intent', { amount, currency });
      setClientSecret(response.data.client_secret);
      setMessage('Payment intent created successfully. You can now confirm the payment.');
    } catch (error) {
      setMessage(`Error: ${error.response?.data.detail || 'Something went wrong'}`);
    }
  };

  const handleConfirmPayment = async () => {
    if (!clientSecret) {
      return setMessage('You must create a payment intent first.');
    }

    try {
      const response = await axios.post('/confirm-payment', { payment_id: clientSecret });
      setMessage(response.data.detail);
    } catch (error) {
      setMessage(`Error: ${error.response?.data.detail || 'Something went wrong'}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <form className="bg-white p-8 rounded shadow-md w-96" onSubmit={handleCreatePaymentIntent}>
        <h2 className="text-2xl font-bold mb-4">Process Payment</h2>
        <div className="mb-4">
          <label htmlFor="amount" className="block text-sm font-medium text-gray-600">Amount</label>
          <input
            id="amount"
            type="number"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="currency" className="block text-sm font-medium text-gray-600">Currency</label>
          <input
            id="currency"
            type="text"
            value={currency}
            onChange={(e) => setCurrency(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Create Payment Intent
        </button>
      </form>

      {clientSecret && (
        <button
          onClick={handleConfirmPayment}
          className="mt-4 bg-green-500 text-white p-2 rounded hover:bg-green-600"
        >
          Confirm Payment
        </button>
      )}

      {message && <p className="mt-4 text-center text-sm text-red-500">{message}</p>}
    </div>
  );
};

export default PaymentForm;