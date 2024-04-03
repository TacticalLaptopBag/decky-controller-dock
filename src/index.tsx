import {
  definePlugin,
  PanelSection,
  PanelSectionRow,
  ServerAPI,
  staticClasses,
  ToggleField,
} from "decky-frontend-lib";
import { useState, VFC } from "react";
import { FaGamepad } from "react-icons/fa";


const Content: VFC<{ serverAPI: ServerAPI }> = ({serverAPI}) => {
  const [isControllerModeOn, setControllerMode] = useState<boolean>(true);
  const [isChangingControllerMode, setChangingControllerMode] = useState<boolean>(true);
  const [isKeyboardModeOn, setKeyboardMode] = useState<boolean>(true);
  const [isChangingKeyboardMode, setChangingKeyboardMode] = useState<boolean>(true);
  const [isMouseModeOn, setMouseMode] = useState<boolean>(true);
  const [isChangingMouseMode, setChangingMouseMode] = useState<boolean>(true);

  serverAPI.callPluginMethod<{}, boolean>('get_state', {}).then((response) => {
    if(response.success) {
      setControllerMode(response.result[0]);
      setKeyboardMode(response.result[1]);
      setMouseMode(response.result[2]);
      setChangingControllerMode(false);
      setChangingKeyboardMode(false);
      setChangingMouseMode(false);
    }
  });

  return (
    <PanelSection title="Controls">
      <PanelSectionRow>
        The built-in Steam Controller will now be disabled whenever one of the selected types of devices are connected.
        If the external device is disconnected, the built-in Steam Controller will be enabled again.
      </PanelSectionRow>
      <ToggleField
        label="Controller"
        checked={isControllerModeOn}
        onChange={(value: boolean) => {
          if(isChangingControllerMode) return;
          setChangingControllerMode(true);

          const methodName = value ? 'enable_functionality' : 'disable_functionality';
          serverAPI.callPluginMethod(methodName, { functionality: "controller" }).then((response) => {
            if(response.success) setChangingControllerMode(value)
          }).finally(() => {
            setChangingControllerMode(false);
          });
        }}
        disabled={isChangingControllerMode}
      >
      </ToggleField>
      
      <ToggleField
        label="Keyboard"
        checked={isKeyboardModeOn}
        onChange={(value: boolean) => {
          if(isChangingKeyboardMode) return;
          setChangingKeyboardMode(true);

          const methodName = value ? 'enable_functionality' : 'disable_functionality';
          serverAPI.callPluginMethod(methodName, { functionality: 'keyboard' }).then((response) => {
            if(response.success) setChangingKeyboardMode(value)
          }).finally(() => {
            setChangingKeyboardMode(false);
          });
        }}
        disabled={isChangingKeyboardMode}
      >
      </ToggleField>

      <ToggleField
        label="Mouse"
        checked={isMouseModeOn}
        onChange={(value: boolean) => {
          if(isChangingMouseMode) return;
          setChangingMouseMode(true);

          const methodName = value ? 'enable_functionality' : 'disable_functionality';
          serverAPI.callPluginMethod(methodName, { functionality: 'mouse' }).then((response) => {
            if(response.success) setChangingMouseMode(value)
          }).finally(() => {
            setChangingMouseMode(false);
          });
        }}
        disabled={isChangingMouseMode}
      >
      </ToggleField>

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
