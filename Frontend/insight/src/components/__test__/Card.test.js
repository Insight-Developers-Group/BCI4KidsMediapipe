import { render, screen } from "@testing-library/react";
import Card from "../Card";

describe('Cards should say "YES" if cardClass is "card_yes" and "NO" if card_class is "card_no"', () => {
    it("should render the yes card", () => {
        render(<Card order="card_first" cardClass="card_yes" />);
        const YesCard = screen.getByText(/YES/i);
        expect(YesCard).toBeInTheDocument();
    });

    it("should render the no card", () => {
        render(<Card order="card_first" cardClass="card_no" />);
        const NoCard = screen.getByText(/NO/i);
        expect(NoCard).toBeInTheDocument();
    });
});

describe("Second cards should be displayed properly", () => {
    it("should render the second yes card", () => {
        render(<Card order="card_second" cardClass="card_yes" />);
        const YesCard = screen.getByText(/YES/i);
        expect(YesCard).toBeInTheDocument();
    });

    it("should render the second no card", () => {
        render(<Card order="card_second" cardClass="card_no" />);
        const NoCard = screen.getByText(/NO/i);
        expect(NoCard).toBeInTheDocument();
    });
});
