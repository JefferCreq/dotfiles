import { App } from "astal/gtk3";
import {
  settingsVisibility,
  userPanelVisibility,
} from "../../../variables";

import hyprland from "gi://AstalHyprland";
import ToggleButton from "../../toggleButton";
import { ClientTitle, Workspaces } from "../modules";
const Hyprland = hyprland.get_default();

function AppLauncher() {
  return (
    <ToggleButton
      className="app-search"
      label=""
      onToggled={(self, on) => App.toggle_window("app-launcher")}
    />
  );
}

function OverView() {
  return (
    <button
      className="overview"
      label="󱗼"
      onClicked={() =>
        Hyprland.message_async("dispatch hyprexpo:expo toggle", (res) =>
          print(res)
        )
      }
    />
  );
}

function Settings() {
  return (
    <ToggleButton
      className="settings"
      label=""
      onToggled={(self, on) => settingsVisibility.set(on)}
    />
  );
}

function UserPanel() {
  return (
    <ToggleButton
      className="user-panel"
      label=""
      onToggled={(self, on) => userPanelVisibility.set(on)}
    />
  );
}

const Actions = () => {
  return (
    <box className="actions">
      <UserPanel />
      <Settings />
      <AppLauncher />
    </box>
  );
};

export default () => {
  return (
    <box className="bar-left" spacing={5}>
      <Actions />
      <OverView />
      <Workspaces />
      <ClientTitle />
    </box>
  );
};
