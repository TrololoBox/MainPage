import { render, screen } from '@testing-library/react';

import ProstoKitHome from '@/ProstoKitHome';

describe('ProstoKitHome', () => {
  it('renders the hero and pricing sections', () => {
    render(<ProstoKitHome />);

    expect(screen.getByText(/мелкие задачи — в один клик\./i)).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /подписка/i })).toBeInTheDocument();
  });
});
