from pypresence import Presence
import time
import psutil
import win32gui

# --- DISCORD RPC SETUP ---
CLIENT_ID = "1390675187669794826"  # Replace with your actual app's client ID
RPC = Presence(CLIENT_ID)
RPC.connect()

start_time = int(time.time())
IDLE_TIMEOUT = 600  # 10 minutes in seconds
last_active_time = time.time()

# --- BUTTON SETUP ---
BUTTONS = [{"label": "HMU", "url": "https://www.instagram.com/prodbyolek/"}]

# --- PLUGIN DETECTION FUNCTION ---
def detect_plugin_windows(max_plugins=2):
    plugin_keywords = [
        "ValhallaDelay", "ValhallaRoom",
        "FabFilter Pro-Q", "Pro-Q", "Pro-L", "Saturn",
        "Serum", "Vital", "Massive X", "Kontakt", "Omnisphere",
        "RC-20", "Decapitator", "EffectRack", "OTT",
        "Soothe2", "ShaperBox", "Neutron", "Ozone",
        "Portal", "SketchCassette", "CamelCrusher",
        "EchoBoy", "Little AlterBoy",
        "Sylenth1", "Nexus", "Diva", "Spire", "Pigments",
        "Massive", "Phase Plant", "Serum FX", "FabFilter Pro-MB",
        "FabFilter Pro-C", "FabFilter Pro-DS", "FabFilter Pro-G",
        "FabFilter Timeless", "FabFilter Volcano", "FabFilter Twin 2",
        "ValhallaVintageVerb", "ValhallaShimmer", "ValhallaFreqEcho",
        "ValhallaSupermassive", "FabFilter Micro", "FabFilter One",
        "FabFilter Simplon", "FabFilter Saturn 2", "FabFilter Pro-R",
        "Waves SSL E-Channel", "Waves SSL G-Master Buss Compressor",
        "Waves CLA-2A", "Waves CLA-76", "Waves H-Delay",
        "Waves L2 Ultramaximizer", "Waves RComp",
        "Waves Renaissance Vox", "Waves C6", "Waves MV2",
        "Waves Vocal Rider", "Waves API 2500",
        "Waves PuigTec EQ", "Waves Abbey Road TG Mastering Chain",
        "Waves Abbey Road Chambers",
        "Soundtoys Decapitator", "Soundtoys EchoBoy", "Soundtoys Crystallizer",
        "Soundtoys Little Radiator", "Soundtoys Little AlterBoy",
        "Soundtoys PanMan", "Soundtoys Tremolator",
        "Soundtoys MicroShift", "Soundtoys Devil-Loc",
        "FabFilter Saturn", "FabFilter Saturn 2",
        "iZotope RX 9", "iZotope Nectar", "iZotope Trash 2",
        "iZotope Stutter Edit", "iZotope Insight", "iZotope Neoverb",
        "iZotope Ozone 9", "iZotope RX Elements",
        "Native Instruments Guitar Rig", "Native Instruments Reaktor",
        "Native Instruments Massive", "Native Instruments Absynth",
        "Native Instruments FM8", "Native Instruments Battery",
        "Native Instruments Kontakt 6",
        "Melodyne", "Auto-Tune Pro", "Waves Tune",
        "Celemony Melodyne 5", "MeldaProduction MEqualizer",
        "MeldaProduction MCompressor", "MeldaProduction MSaturator",
        "MeldaProduction MLimiter",
        "Xfer Records LFOTool", "Xfer Records Cthulhu",
        "Xfer Records Nerve", "Xfer Records OTT",
        "FabFilter Lush", "FabFilter Twin 2",
        "Output Exhale", "Output Portal", "Output Movement",
        "Output Rev", "Output Analog Strings",
        "LennarDigital Sylenth1", "Reveal Sound Spire",
        "Arturia Pigments", "Arturia V Collection",
        "Arturia Analog Lab",
        "Korg Wavestate Native", "Korg M1 Le",
        "D16 Group Decimort 2", "D16 Group PunchBox",
        "D16 Group Drumazon", "D16 Group Devastor 2",
        "D16 Group Sigmund",
        "Softube Console 1", "Softube Tape",
        "Softube Saturation Knob", "Softube Harmonics",
        "Softube Modular", "Softube Heartbeat",
        "XLN Audio Addictive Drums", "XLN Audio Addictive Keys",
        "XLN Audio RC-20 Retro Color",
        "Celemony Melodyne Studio", "Celemony Melodyne Assistant",
        "Brainworx bx_digital V3", "Brainworx bx_console SSL 4000",
        "Brainworx bx_subfilter", "Brainworx bx_masterdesk",
        "Brainworx bx_saturator V2",
        "Slate Digital Virtual Mix Rack", "Slate Digital Virtual Tape Machines",
        "Slate Digital FG-X", "Slate Digital Virtual Console",
        "Slate Digital Trigger 2", "Slate Digital Verbsuite",
        "Eventide H3000 Factory", "Eventide Blackhole",
        "Eventide Physion", "Eventide Ultraharmonizer",
        "Eventide Elevate", "Eventide MangledVerb",
        "U-He Diva", "U-He Zebra2", "U-He Hive",
        "U-He Bazille", "U-He ACE",
        "Kilohearts Phase Plant", "Kilohearts Snap Heap",
        "Kilohearts Multipass", "Kilohearts Disperser",
        "Kilohearts Chorus", "Kilohearts Delay",
        "ValhallaPlate", "ValhallaVintageVerb",
        "Tokyo Dawn Labs TDR Nova", "Tokyo Dawn Labs TDR Kotelnikov",
        "Tokyo Dawn Labs TDR SlickEQ",
        "Cableguys ShaperBox", "Cableguys Curve 2",
        "Cableguys HalfTime", "Cableguys Pancake 2",
        "FabFilter Pro-DS", "FabFilter Pro-C 2",
        "FabFilter Timeless 3", "FabFilter Volcano 3",
        "Native Instruments FM8", "Native Instruments Absynth 5",
        "Spectrasonics Trilian", "Spectrasonics Keyscape",
        "Spectrasonics Omnisphere 2",
        "MeldaProduction MAutopan", "MeldaProduction MFlanger",
        "MeldaProduction MChorus",
        "Softube Tube-Tech CL 1B", "Softube Summit Audio TLA-100A",
        "Softube Empirical Labs EL8 Distressor",
        "Softube Weiss Compressor/Limiter",
        "Sound Radix Auto-Align", "Sound Radix Drum Leveler",
        "Sound Radix 32 Lives",
        "Eventide H910 Harmonizer", "Eventide H949",
        "Slate Digital FG-N", "Slate Digital VCC",
        "Plugin Alliance bx_cleansweep", "Plugin Alliance bx_masterdesk",
        "Plugin Alliance SPL Vitalizer",
        "Plugin Alliance Maag EQ4",
        "Plugin Alliance Elysia Nvelope",
        "Plugin Alliance Lindell 354E",
        "Plugin Alliance Lindell 80 Series",
        "Plugin Alliance Brainworx bx_digital V3",
        "Plugin Alliance Shadow Hills Mastering Compressor",
        "Native Instruments Massive X", "Native Instruments Kontakt 7",
        "Arturia Jup-8 V", "Arturia CS-80 V",
        "Arturia Mini V",
        "Sugar Bytes Effectrix", "Sugar Bytes DrumComputer",
        "Sugar Bytes Cyclop",
        "Output Signal", "Output Substance",
        "Output Analog Brass & Winds",
        "Heavyocity Damage", "Heavyocity Gravity",
        "Heavyocity Forzo",
        "MeldaProduction MMultiBandStereoProcessor",
        "MeldaProduction MAnalyzer",
        "MeldaProduction MDrummer",
        "Waves PuigChild 670", "Waves Kramer Master Tape",
        "Waves H-Comp", "Waves H-EQ",
        "Waves H-Reverb", "Waves H-Delay Hybrid",
        "Waves Vocal Bender",
        "Waves Element 2.0", "Waves Codex",
        "Waves Abbey Road TG Mastering Chain",
        "Waves Scheps Omni Channel",
        "Waves Abbey Road Chambers",
        "Waves Abbey Road Plates",
        "Waves Abbey Road Reverb Plates",
        "Waves Abbey Road J37 Tape",
        "U-He Satin", "U-He Protoverb",
        "U-He Presswerk",
        "MeldaProduction MTransientProcessor", "MeldaProduction MAutoAlign",
        "MeldaProduction MAutoVolume",
        "MeldaProduction MFreeformEqualizer",
        "ValhallaDelay 2", "ValhallaShimmer 2",
        "ValhallaRoom 2",
        "FabFilter Saturn 3", "FabFilter Pro-Q 3",
        "FabFilter Pro-C 3", "FabFilter Pro-MB 2",
        "FabFilter Pro-L 2", "FabFilter Pro-G 2",
        "FabFilter Pro-R 2",
        "Soundtoys Decapitator 2", "Soundtoys EchoBoy 2",
        "Soundtoys Crystallizer 2",
        "Output Portal 2", "Output Movement 2",
        "Output Rev 2",
        "Xfer Records Serum 2", "Xfer Records LFOTool 2",
        "Xfer Records OTT 2",
        "Eventide Blackhole 2",
        "Eventide H3000 Factory 2",
        "Native Instruments Kontakt 6",
        "Melodyne 5 Studio",
        "Celemony Melodyne 5 Editor",
        "FabFilter Simplon 2",
        "MeldaProduction MMultiBandDynamics",
        "MeldaProduction MStereoProcessor",
        "MeldaProduction MNoiseGenerator",
        "Waves NS1",
        "Waves Vocal Rider 2",
        "Waves Vitamin",
        "iZotope Nectar 3 Plus",
        "iZotope Trash 3",
        "iZotope Neutron 3 Advanced",
        "iZotope Ozone 10 Advanced",
        "iZotope RX 10 Standard",
        "XLN Audio Addictive Drums 2",
        "XLN Audio XO",
        "FabFilter Saturn 3",
        "Arturia Syntronik",
        "Arturia DX7 V",
        "Arturia CZ V",
        "Arturia Prophet V",
        "Kush Audio UBK-1",
        "Kush Audio Electra DSP",
        "Softube Saturation Knob",
        "Softube Console 1 Fader",
        "Soundtoys Little AlterBoy 2",
        "Soundtoys Devil-Loc Deluxe",
        "Soundtoys PanMan 2",
        "Cableguys ShaperBox 2",
        "Cableguys Curve 3",
        "FabFilter Pro-Q 3",
        "FabFilter Timeless 3",
        "FabFilter Volcano 3",
        "U-He Diva 2",
        "U-He Zebra2 2",
        "U-He Hive 2",
        "Kilohearts Phase Plant 2",
        "Kilohearts Multipass 2",
        "Kilohearts Snap Heap 2",
        "Kilohearts Disperser 2",
        "Tokyo Dawn Labs TDR Nova GE",
        "Tokyo Dawn Labs TDR Kotelnikov GE",
        "Tokyo Dawn Labs TDR SlickEQ GE",
        "Brainworx bx_digital V3",
        "Brainworx bx_console N",
        "Brainworx bx_console SSL 4000 E",
        "Brainworx bx_subfilter 2",
        "Brainworx bx_masterdesk 2",
        "Slate Digital Virtual Mix Rack 2",
        "Slate Digital FG-X 2",
        "Slate Digital VCC 2",
        "Eventide Elevate 2",
        "Eventide Physion 2",
        "Eventide MangledVerb 2",
        "Native Instruments FM8 2",
        "Native Instruments Absynth 5 2",
        "Native Instruments Battery 4",
        "Native Instruments Kontakt 7",
        "MeldaProduction MEqualizer 2",
        "MeldaProduction MCompressor 2",
        "MeldaProduction MSaturator 2",
        "MeldaProduction MLimiter 2",
        "ZENOLOGY",
        "Keyscape",
        "Analog Lab V",
    ]

    found_plugin = None

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            for plugin in plugin_keywords:
                if plugin.lower() in title.lower():
                    nonlocal found_plugin
                    found_plugin = plugin
                    return

    win32gui.EnumWindows(callback, None)
    return found_plugin

# --- RENDERING DETECTION FUNCTION ---
def is_rendering_audio():
    def callback(hwnd, found):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Export Audio/Video" in title:
                found.append(True)
    result = []
    win32gui.EnumWindows(callback, result)
    return bool(result)

# --- ABLETON PROJECT DETECTION ---
def get_ableton_project_name():
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Ableton Live" in title:
                extra.append(title)
    titles = []
    win32gui.EnumWindows(callback, titles)
    if titles:
        return titles[0].replace(" - Ableton Live 12 Suite", "").strip()
    return "No Project"

def is_ableton_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "Ableton Live" in proc.info['name']:
            return True
    return False

# --- MAIN LOOP ---
while True:
    current_time = time.time()

    if is_ableton_running():
        if is_rendering_audio():
            RPC.update(
                details="Ableton Live 12 Suite",
                state="Rendering Audio...",
                start=start_time,
                large_image="ableton_logoo",
                large_text="Ableton Live 12",
                buttons=BUTTONS
            )
            last_active_time = current_time

        else:
            project_name = get_ableton_project_name()
            plugin = detect_plugin_windows()

            if plugin:
                state_line = f"Using {plugin}"
            else:
                state_line = "Arranging Sounds"

            # Check if user has been idle
            if current_time - last_active_time > IDLE_TIMEOUT:
                RPC.update(
                    details="Ableton Live 12 Suite",
                    state="Idle",
                    start=start_time,
                    large_image="idle_image",  # Optional idle image
                    large_text="Idle in Ableton",
                    buttons=BUTTONS
                )
            else:
                # Choose image based on plugin
                if plugin and plugin.lower() == "valhalladelay":
                    large_image = "valhalladelay_rp"
                else:
                    large_image = "ableton_logo"

                RPC.update(
                    details="Ableton Live 12 Suite",
                    state=f"{state_line} in {project_name}.alp",
                    start=start_time,
                    large_image=large_image,
                    large_text="Ableton Live 12",
                    buttons=BUTTONS
                )

            # Reset idle timer regardless of plugin use
            last_active_time = current_time

    else:
        RPC.clear()

    time.sleep(15)