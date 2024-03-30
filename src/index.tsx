import {
  definePlugin,
  PanelSection,
  ServerAPI,
  staticClasses,
} from "decky-frontend-lib";
import { VFC } from "react";
import { FaGamepad } from "react-icons/fa";


const Content: VFC<{ serverAPI: ServerAPI }> = ({serverAPI}) => {
  return (
    <PanelSection title="Panel Section">
      Controller Dock is installed!
      The built-in Steam Controller will now be disabled whenever an external controller is connected.
      If the external controller is disconnected, the built-in Steam Controller will be enabled again.
    </PanelSection>
  );
};

export default definePlugin((serverApi: ServerAPI) => {
  return {
    title: <div className={staticClasses.Title}>Controller Dock</div>,
    content: <Content serverAPI={serverApi} />,
    icon: <FaGamepad />,
  };
});
