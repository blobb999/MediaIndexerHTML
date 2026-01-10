# 🎵 Crossfade Plugin for MediaIndexerHTML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.3-blue.svg)](https://github.com/blobb999/MediaIndexerHTML/tree/main/plugins/crossfade)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A professional audio crossfade plugin for [MediaIndexerHTML](https://github.com/blobb999/MediaIndexerHTML) that provides seamless transitions between audio tracks with configurable fade curves and intelligent audio state management.

## 🥄 The "Spoon Principle"

This plugin implements a unique **"One Spoon, Always Pass It On"** architecture (Löffel-Prinzip):
- Only **ONE** audio player holds the "spoon" (is active) at any time
- When a new track starts, the spoon is smoothly passed from the old player to the new one
- Prevents audio chaos, memory leaks, and ghost players
- Ensures clean state transitions without audio artifacts

## ✨ Features

### Core Functionality
- 🎚️ **True Crossfading**: Seamless audio blending between tracks (not just stop→start)
- 📊 **Multiple Fade Curves**: 
  - **Linear**: Uniform, neutral transitions
  - **Exponential**: Smooth, professional (like Spotify)
  - **Logarithmic**: Dynamic, dramatic transitions
- ⏱️ **Configurable Duration**: Adjustable fade time from 1 to 10 seconds
- 🔄 **Smart Preloading**: Optional next-track preloading for gapless playback
- 🎯 **Precise Timing**: Automatically triggers crossfade based on remaining track duration

### Technical Highlights
- 🥄 **Single Audio Instance Management**: State machine prevents multiple simultaneous players
- 🔌 **Hook Reusability**: Event listeners are intelligently transferred to new audio instances
- 🎵 **Autoplay Integration**: Respects global autoplay settings
- 💾 **Persistent Settings**: All preferences automatically saved to database
- 🐛 **Extensive Logging**: Emoji-based debug output for easy troubleshooting

## 📦 Installation

1. Navigate to your MediaIndexerHTML plugins directory:
```bash
cd MediaIndexerHTML/plugins
```

2. Clone or download this plugin:
```bash
git clone https://github.com/blobb999/MediaIndexerHTML.git
# Or manually download and place in plugins/crossfade/
```

3. Ensure the plugin structure:
```
plugins/
└── crossfade/
    └── __init__.py
```

4. Restart MediaIndexerHTML - the plugin will auto-register

## 🎮 Usage

### Basic Setup

1. **Open Settings** in MediaIndexerHTML
2. Navigate to the **Crossfade Plugin** section
3. Configure your preferences:
   - ✅ Enable/Disable crossfading
   - ⏱️ Adjust fade duration (slider: 1-10s)
   - 📊 Select fade curve (Linear/Exponential/Logarithmic)
   - 🔄 Toggle next-track preloading

### Settings Interface
```
┌─────────────────────────────────────────┐
│ 🎵 Crossfade Plugin v2.3 🥄            │
├─────────────────────────────────────────┤
│ ☑ Crossfade aktivieren                  │
│                                         │
│ Überblend-Dauer: [====●====] 5s        │
│                                         │
│ Fade-Kurve: [Exponential ▼]            │
│                                         │
│ ☑ Nächstes Audio vorladen               │
│                                         │
│ Status: Aktiv 🥄 | Dauer: 5s           │
│         Kurve: Exponential              │
└─────────────────────────────────────────┘
```

### How It Works

1. **Track Playing**: Current audio has the "spoon" 🥄
2. **Crossfade Trigger**: When remaining time ≤ fade duration + 0.5s
3. **Next Track Loads**: New audio element created with volume = 0
4. **Crossfade Start**: Both tracks play simultaneously
5. **Volume Transition**: 
   - Old track: 100% → 0% (fade out)
   - New track: 0% → 100% (fade in)
6. **Spoon Transfer**: Old player stops, new player gets the spoon 🥄
7. **Hook Reattachment**: Event listeners transferred to new player
8. **Repeat**: Process continues for next transition

## 🔧 Configuration

### Available Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | Boolean | `true` | Enable/disable crossfading |
| `fadeDuration` | Float | `3.0` | Fade duration in seconds (1.0 - 10.0) |
| `fadeCurve` | String | `"exponential"` | Fade curve type (`linear`, `exponential`, `logarithmic`) |
| `preloadNext` | Boolean | `true` | Preload next track for better performance |

### Fade Curves Explained

#### Linear
```
Volume
100% │\
     │ \
     │  \
  0% │___\
     0s  8s
```
- Uniform volume change
- Neutral sound
- Can feel abrupt in the middle

#### Exponential (Recommended)
```
Volume
100% │\
     │ \___
     │     \___
  0% │_________\
     0s        8s
```
- Slow start, fast finish
- Professional sound (like Spotify)
- Most pleasant for music

#### Logarithmic
```
Volume
100% │\___
     │\   \___
     │ \      \___
  0% │___________\
     0s          8s
```
- Fast start, slow finish
- Dramatic transitions
- Good for DJ-style mixing

## 🔬 Technical Details

### Architecture
```
┌─────────────────────────────────────────────┐
│          Crossfade Plugin Core              │
├─────────────────────────────────────────────┤
│  🥄 Spoon State Machine                     │
│  ├─ currentAudio (spoon owner)              │
│  ├─ nextAudio (waiting for spoon)           │
│  └─ isCrossfading (transition flag)         │
│                                             │
│  🎚️ Volume Management                       │
│  ├─ baseVolume (user setting)               │
│  ├─ fadeOut curve calculation               │
│  └─ fadeIn curve calculation                │
│                                             │
│  🔌 Hook Management                          │
│  ├─ attachSpoonHooks()                      │
│  ├─ timeupdate listener                     │
│  ├─ ended listener                          │
│  └─ metadata listener                       │
│                                             │
│  ⚙️ Settings Sync                           │
│  ├─ loadSettingsFromDOM()                   │
│  ├─ reloadSettingsFromDOM()                 │
│  └─ updateSettings()                        │
└─────────────────────────────────────────────┘
```

### Key Functions

#### `handlePlayAudio(filepath, title, category)`
Main entry point - manages spoon transfer when new track starts

#### `startCrossfade()`
Initiates crossfade transition between current and next audio

#### `performFade()`
Recursive function using `requestAnimationFrame` for smooth volume transitions

#### `completeCrossfade()`
Finalizes transition, transfers spoon, reattaches hooks

#### `attachSpoonHooks(audio)`
Attaches event listeners to audio element for crossfade detection and autoplay

### Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

**Requirements:**
- Modern JavaScript (ES6+)
- Web Audio API support
- `requestAnimationFrame` support

## 🐛 Debugging

The plugin includes extensive emoji-based logging:
```javascript
🔌 CrossfadePlugin: Plugin wird geladen...
🥄 LÖFFEL-PRINZIP: Immer nur EIN Player hat den Löffel!
🎵 Crossfade: Initializing LÖFFEL-SYSTEM...
🥄 Loading settings from DOM...
✅ Crossfade Plugin v2.3: LÖFFEL-SYSTEM fully loaded!
```

Enable browser console to see detailed state transitions:
- 🥄 Spoon transfers
- 🔥 Crossfade triggers
- ✅ Successful operations
- ❌ Errors and warnings

## 🤝 Contributing

Contributions are welcome! This plugin is part of the larger [MediaIndexerHTML](https://github.com/blobb999/MediaIndexerHTML) project.

### Areas for Improvement
- [ ] Additional fade curves (Sigmoid, Equal-Power)
- [ ] Crossfade visualization in UI
- [ ] Per-genre curve presets
- [ ] Manual crossfade trigger
- [ ] Fade duration per track/playlist

## 📝 License

MIT License

Copyright (c) 2025 blobb999

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🔗 Links

- **Main Project**: [MediaIndexerHTML](https://github.com/blobb999/MediaIndexerHTML)
- **Plugin Directory**: [plugins/crossfade](https://github.com/blobb999/MediaIndexerHTML/tree/main/plugins/crossfade)
- **Issues**: [Report bugs](https://github.com/blobb999/MediaIndexerHTML/issues)

## 👨‍💻 Author

**blobb999**
- GitHub: [@blobb999](https://github.com/blobb999)
- Project: [MediaIndexerHTML](https://github.com/blobb999/MediaIndexerHTML)

---

⭐ If you find this plugin useful, please star the [main project](https://github.com/blobb999/MediaIndexerHTML)!

🥄 *Remember: Only one spoon, always pass it on!*