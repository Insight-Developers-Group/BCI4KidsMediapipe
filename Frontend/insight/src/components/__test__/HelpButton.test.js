import { fireEvent, render, screen } from '@testing-library/react';
import HelpButton from '../HelpButton.js';
import HelpMenu from '../HelpMenu.js'

describe("Testing the help button", () => {
    it('should render the help icon', () => {
        render(<HelpButton />);
        const HelpButtonIcon = screen.getByAltText(/help-icon/i);
        expect(HelpButtonIcon.getAttribute("src")).toMatch(new RegExp('helplogo.svg'));
    });

    it('should render the help button background', () => {
        render(<HelpButton />);
        const HelpButtonBackground = screen.getByTestId("helpIconBgrnd")
        expect(HelpButtonBackground).toBeInTheDocument();
    });

    it('should render the help menu', () => {
        render(<HelpMenu />);
        const helpMenu = screen.getByTestId("help-menu")
        expect(helpMenu).toBeInTheDocument();
    });

    it('should open when clicked once, then close when clicked again', () => {
        render(<HelpButton />);
        render(<HelpMenu />);
        const helpMenu = screen.getByTestId("help-menu")
        const HelpMenuOverlayClose = screen.getByTestId("help-menu-overlay-close")
        fireEvent.click(screen.getByTestId("helpIconBgrnd"))
        expect(HelpMenu).toBeVisible();
        fireEvent.click(HelpMenuOverlayClose)
        expect(HelpMenu).not.toBeVisible();
    });
})
