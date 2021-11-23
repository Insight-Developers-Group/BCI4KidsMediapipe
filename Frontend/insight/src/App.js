import Button from './components/Button';
import MenuButton from './components/MenuButton';
import Menu from './components/Menu';
import UploadData from './components/UploadData';
import HelpButton from './components/HelpButton';
import HelpMenu from './components/HelpMenu';
import ReloadButton from './components/ReloadButton';
import VideoDisplay from './components/VideoDisplay';
import ModeButton from './components/ModeButton';
import ModeSwitcher from './components/ModeSwitcher';
import CardStack from './components/CardStack';
import Card from './components/Card';

function App() {
  return (
    <div className="App">
      <p>~~~~ Test Default Text ~~~~</p>
      <MenuButton />
      <HelpButton />
      <ReloadButton />
      <VideoDisplay />
      <ModeSwitcher />
      <CardStack />
      
    </div>
  );
}

export default App;
