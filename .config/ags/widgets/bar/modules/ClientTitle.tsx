import { Gtk } from "astal/gtk3";
import { emptyWorkspace, focusedClient, globalTransition } from "../../../variables";
import { bind } from "../../../../../../../usr/share/astal/gjs";

export default function ClientTitle() {
  return (
    <revealer
      revealChild={emptyWorkspace.as((empty) => !empty)}
      transitionDuration={globalTransition}
      transitionType={Gtk.RevealerTransitionType.SLIDE_RIGHT}
      child={focusedClient.as(
        (client) =>
          client && (
            <label
              className="client-title"
              truncate={true}
              max_width_chars={32}
              label={bind(client, "title").as(String)}
            />
          )
      )}
    ></revealer>
  );
}
