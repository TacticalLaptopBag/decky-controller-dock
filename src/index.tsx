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
  const [isEnabled, setEnabled] = useState<boolean>(true);
  let changingEnabled = false;

  serverAPI.callPluginMethod<{}, boolean>("is_enabled", {}).then((response) => {
    if(response.success) {
      setEnabled(response.result)
    }
  })

  return (
    <PanelSection>
      <PanelSectionRow>
      <ToggleField
        label="Disable Deck Controller while External Controller connected"
        checked={isEnabled}
        onChange={(value: boolean) => {
          if(changingEnabled) return
          changingEnabled = true;

          if(value) {
            serverAPI.callPluginMethod("enable", {}).then((response) => {
              if(response.success) setEnabled(true)
            }).finally(() => {
              changingEnabled = false;
            });
          } else {
            serverAPI.callPluginMethod("disable", {}).then((response) => {
              if(response.success) setEnabled(false)
            }).finally(() => {
              changingEnabled = false;
            })
          }
        }}
      >
      </ToggleField>
      </PanelSectionRow>
    </PanelSection>
  );
};

// const DeckyPluginRouterTest: VFC = () => {
//   return (
//     <div style={{ marginTop: "50px", color: "white" }}>
//       Hello World!
//       <DialogButton onClick={() => Navigation.NavigateToLibraryTab()}>
//         Go to Library
//       </DialogButton>
//     </div>
//   );
// };

export default definePlugin((serverApi: ServerAPI) => {
  // serverApi.routerHook.addRoute("/decky-nav-test", DeckyPluginRouterTest, {
  //   exact: true,
  // });

  return {
    title: <div className={staticClasses.Title}>Controller Dock</div>,
    content: <Content serverAPI={serverApi} />,
    icon: <FaGamepad />,
    // onDismount() {
    //   serverApi.routerHook.removeRoute("/decky-nav-test");
    // },
  };
});
