import { fireEvent, render, screen } from "@testing-library/react";
import CardStack from "../CardStack";

it("should render the card stack", () => {
    render(<CardStack />);
    const CardStk = screen.getByTestId("card_stack");
    expect(CardStk).toBeInTheDocument();
});

describe("Different combinations of cards should each render properly", () => {
    it("should correctly display none / none cards", () => {
        render(<CardStack firstCard="card_none" secondCard="card_none" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        expect(FirstCard).not.toBeVisible();
        expect(SecondCard).not.toBeVisible();
    });

    it("should correctly display yes / none cards", () => {
        render(<CardStack firstCard="card_yes" secondCard="card_none" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("Yes");
        expect(CardLabels[1]).toHaveTextContent("");
    });

    it("should correctly display no / none cards", () => {
        render(<CardStack firstCard="card_no" secondCard="card_none" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("No");
        expect(CardLabels[1]).toHaveTextContent("");
    });

    it("should correctly display Yes / Yes cards", () => {
        render(<CardStack firstCard="card_yes" secondCard="card_yes" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("Yes");
        expect(CardLabels[1]).toHaveTextContent("Yes");
    });

    it("should correctly display Yes / No cards", () => {
        render(<CardStack firstCard="card_yes" secondCard="card_no" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("Yes");
        expect(CardLabels[1]).toHaveTextContent("No");
    });

    it("should correctly display No / Yes cards", () => {
        render(<CardStack firstCard="card_no" secondCard="card_yes" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("No");
        expect(CardLabels[1]).toHaveTextContent("Yes");
    });

    it("should correctly display No / No cards", () => {
        render(<CardStack firstCard="card_no" secondCard="card_no" />);
        const FirstCard = screen.getByTestId("first_card");
        expect(FirstCard).toBeInTheDocument();
        const SecondCard = screen.getByTestId("second_card");
        expect(SecondCard).toBeInTheDocument();

        const CardLabels = screen.getAllByTestId("card_label");
        expect(CardLabels[0]).toHaveTextContent("No");
        expect(CardLabels[1]).toHaveTextContent("No");
    });
});
