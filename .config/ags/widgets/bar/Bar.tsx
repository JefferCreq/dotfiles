import { App, Astal, Gdk } from "astal/gtk3";
import { bind } from "astal";
import barLeft from "./components/barLeft";
import barMiddle from "./components/barMiddle";
import barRight from "./components/barRight";
import {
  barLock,
  barOrientation,
  barVisibility,
  emptyWorkspace,
  globalMargin,
} from "../../variables";

export default () => {
  return (
    <window
      name="bar"
      namespace="bar"
      className="Bar"
      application={App}
      exclusivity={Astal.Exclusivity.EXCLUSIVE}
      layer={Astal.Layer.TOP}
      anchor={bind(barOrientation).as((orientation) =>
        orientation
          ? Astal.WindowAnchor.TOP |
            Astal.WindowAnchor.LEFT |
            Astal.WindowAnchor.RIGHT
          : Astal.WindowAnchor.BOTTOM |
            Astal.WindowAnchor.LEFT |
            Astal.WindowAnchor.RIGHT
      )}
      margin={emptyWorkspace.as((empty) => (empty ? globalMargin : 0))}
      visible={bind(barVisibility)}
      child={
        <eventbox
          // onLeaveNotifyEvent={(self, event: Gdk.Event) => {
          //   const [_, x, y] = event.get_root_coords();
          //   if (y >= 25 && !barLock.get()) {
          //     barVisibility.set(false);
          //   }
          // }}
          onHoverLost={() => {
            if (!barLock.get()) barVisibility.set(false);
          }}
          child={
            <centerbox
              className={emptyWorkspace.as((empty) =>
                empty ? "bar empty" : "bar full"
              )}
              startWidget={<box name="start-widget" child={barLeft()}></box>}
              centerWidget={
                <box name="center-widget" child={barMiddle()}></box>
              }
              endWidget={
                <box name="end-widget" child={barRight()}></box>
              }></centerbox>
          }></eventbox>
      }></window>
  );
};
