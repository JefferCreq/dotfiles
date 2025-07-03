import Cava from "gi://AstalCava";
const cava = Cava.get_default()!;

import { date_less, date_more, globalTransition } from "../../../variables";
import { bind, Variable } from "../../../../../../../usr/share/astal/gjs";
import { Gtk } from "astal/gtk3";
import CustomRevealer from "../../CustomRevealer";

cava?.set_bars(12);
const bars = Variable("");
const blocks = [
  "\u2581",
  "\u2582",
  "\u2583",
  "\u2584",
  "\u2585",
  "\u2586",
  "\u2587",
  "\u2588",
];

function AudioVisualizer() {
  const revealer = (
    <revealer
      // reveal_child={bind(
      //   mpris.players.find(
      //     (player) => player.playbackStatus === Mpris.PlaybackStatus.PLAYING
      //   ) || mpris.players[0],
      //   "playbackStatus"
      // ).as((status) => status === Mpris.PlaybackStatus.PLAYING)}
      revealChild={false}
      transitionDuration={globalTransition}
      transitionType={Gtk.RevealerTransitionType.SLIDE_LEFT}
      child={
        <label
          className={"cava"}
          onDestroy={() => bars.drop()}
          label={bind(bars)}
        />
      }
    />
  );

  cava?.connect("notify::values", () => {
    const values = cava.get_values();
    const blocksLength = blocks.length;
    const barArray = new Array(values.length);

    for (let i = 0; i < values.length; i++) {
      const val = values[i];
      const index = Math.min(Math.floor(val * 8), blocksLength - 1);
      barArray[i] = blocks[index];
    }

    const b = barArray.join("");
    bars.set(b);

    revealer.reveal_child = b !== "".padEnd(12, "\u2581");
  });

  return revealer;
}

function Clock() {
  const revealer = <label className="revealer" label={bind(date_more)}></label>;

  const trigger = <label className="trigger" label={bind(date_less)}></label>;

  return CustomRevealer(trigger, revealer, "clock");
}

function Bandwidth() {
  const bandwidth = Variable("").watch(
    `bash ./scripts/bandwidth.sh`,
    (out) => "↑" + JSON.parse(out)[0] + " ↓" + JSON.parse(out)[1]
  );

  const icon = <icon icon="network-wired-symbolic" />;
  const label = <label label={bind(bandwidth)}></label>;

  return (
    <box className="bandwidth" child={label}>
      {/* {icon} */}
    </box>
  );
}

export default () => {
  return (
    <box className="bar-middle" spacing={5}>
      {/* <CavaWidget /> */}
      {/* <AudioVisualizer /> */}
      {/* <Media /> */}
      <Clock />
      {/* <Bandwidth /> */}
      {/* <ClientTitle /> */}
    </box>
  );
};
