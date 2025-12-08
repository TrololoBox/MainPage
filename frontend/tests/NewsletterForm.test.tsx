import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import { NewsletterForm } from '@/components/NewsletterForm';

describe('NewsletterForm', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  it('submits subscription and shows success message', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({ ok: true, json: async () => ({ id: 1 }) });

    render(<NewsletterForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByLabelText(/имя/i), { target: { value: 'Мария' } });

    fireEvent.click(screen.getByRole('button', { name: /подписаться/i }));

    await waitFor(() => {
      expect(screen.getByText(/готово!/i)).toBeInTheDocument();
    });
  });

  it('disables submit when name is too short', () => {
    render(<NewsletterForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByLabelText(/имя/i), { target: { value: 'A' } });

    expect(screen.getByRole('button', { name: /подписаться/i })).toBeDisabled();
  });
});
