import { fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'
import ModeSwitcher from '../ModeSwitcher';

const mokeFn = jest.fn()

describe('Test mode switch buttons and current mode label are rendered', () => {
    it('should render the face and eye tracking icons', () => {
        render(<ModeSwitcher mode="face" changeMode={mokeFn} />);
        const Girllogo = screen.getByAltText(/girllogo/i);
        expect(Girllogo.getAttribute("src")).toMatch(new RegExp('girllogo.svg'));
        const Eyelogo = screen.getByAltText(/eyelogo/i);
        expect(Eyelogo.getAttribute("src")).toMatch(new RegExp('iris-light.svg'));
    });

    it('should render the face and eye tracking icon backgrounds', () => {
        render(<ModeSwitcher mode="face" changeMode={mokeFn} />);
        const FaceTrackingBtnBgrnd = screen.getByTestId('girlBgrnd')
        expect(FaceTrackingBtnBgrnd).toBeInTheDocument();
        const EyeTrackingBtnBgrnd = screen.getByTestId('eyeBgrnd')
        expect(EyeTrackingBtnBgrnd).toBeInTheDocument();
    });
    it('should render the mode label', () => {
        render(<ModeSwitcher mode="face" changeMode={mokeFn} />);
        const ModeLabel = screen.getByTestId('para')
        expect(ModeLabel).toHaveTextContent('Face Tracking');
    })
})

describe('Clicking on either tracking mode buttons changes the tracking mode label', () => {
    it('should change the tracking label to "Eye Tracking" when the eye tracking button is clicked and should change back to "Face Tracking when the face tracking button is clicked"',
        () => {
            render(<ModeSwitcher mode="face" changeMode={mokeFn} />);
            const EyeTrackingBtnBgrnd = screen.getByTestId('eyeBgrnd')
            const FaceTrackingBtnBgrnd = screen.getByTestId('girlBgrnd')
            fireEvent.click(EyeTrackingBtnBgrnd)
            const ModeLabel = screen.getByTestId('para')
            expect(ModeLabel).toHaveTextContent('Eye Tracking');
            fireEvent.click(FaceTrackingBtnBgrnd)
            expect(ModeLabel).toHaveTextContent('Face Tracking');
        })
})