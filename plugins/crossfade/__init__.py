# -*- coding: utf-8 -*-
"""
🎵 CROSSFADE PLUGIN - FIXED LÖFFEL-ÜBERGABE VERSION
🎶 "Nur ein Löffel, immer weitergeben!"
"""

import json

class CrossfadePlugin:
    def __init__(self):
        self.name = "CrossfadePlugin"
        self.version = "2.3"  # 🥄 Löffel-Edition!
        
        self.enabled = True
        self.fade_duration = 3.0
        self.fade_curve = "exponential"
        self.preload_next = True
        
        print(f"🧩 {self.name} v{self.version} - LÖFFEL-SYSTEM initialisiert")
        print(f"   🥄 Regel: Nur EIN Löffel, immer weitergeben!")
    
    def load_settings(self, settings_dict):
        """Plugin Settings laden."""
        if not isinstance(settings_dict, dict):
            return False
        
        for key, value in settings_dict.items():
            if key == 'plugin.crossfade.enabled':
                self.enabled = bool(value) if value is not None else True
            elif key == 'plugin.crossfade.duration':
                try:
                    if value is not None:
                        self.fade_duration = float(value)
                        print(f"🔧 LOADED fade_duration: {self.fade_duration}s (from value: {value})")
                    else:
                        self.fade_duration = 3.0
                        print(f"🔧 DEFAULT fade_duration: 3.0s (value was None)")
                except Exception as e:
                    print(f"🔧 ERROR loading fade_duration: {e}")
                    self.fade_duration = 3.0
            elif key == 'plugin.crossfade.curve':
                if value in ['linear', 'exponential', 'logarithmic']:
                    self.fade_curve = str(value)
                else:
                    self.fade_curve = 'exponential'
            elif key == 'plugin.crossfade.preload':
                self.preload_next = bool(value) if value is not None else True
        
        print(f"🥄 Final loaded settings: enabled={self.enabled}, duration={self.fade_duration}s, curve={self.fade_curve}")
        return True

    def register(self, plugin_manager):
        """Registriert sich beim Plugin Manager."""
        print(f"🎵 {self.name}: Registriere Hooks...")
        
        plugin_manager.register_hook('html.header', self.inject_javascript)
        plugin_manager.register_hook('html.settings', self.get_settings_html)
        plugin_manager.register_hook('settings.save', self.save_settings)
        plugin_manager.register_hook('settings.load', self.load_settings)
        
        print(f"✅ {self.name}: Hooks registriert - LÖFFEL-SYSTEM aktiv!")
        return True
        
    def inject_javascript(self):
        """JavaScript-Code für Crossfade - LÖFFEL-ÜBERGABE VERSION."""
        
        js_code = f'''<script>
// 🎵 {self.name} v{self.version} - LÖFFEL-ÜBERGABE SYSTEM
// 🥄 NUR EIN LÖFFEL, IMMER WEITERGEBEN!

(function() {{
    'use strict';
    
    console.log('🔌 {self.name}: Plugin wird geladen...');
    console.log('🥄 LÖFFEL-PRINZIP: Immer nur EIN Player hat den Löffel!');
    
    // 1. SOFORT: Original-Funktionen speichern VOR der Wrapper-Erstellung
    const originals = {{
        playAudio: null,
        togglePlay: window.togglePlay,
        closeAudioPlayer: window.closeAudioPlayer,
        seekAudio: window.seekAudio,
        playNextMedia: window.playNextMedia,
        getNextMediaInQueue: window.getNextMediaInQueue,
        addToHistory: window.addToHistory
    }};
    
    // Speichere die ORIGINALE playAudio Funktion
    if (window.playAudio && typeof window.playAudio === 'function') {{
        originals.playAudio = window.playAudio;
        console.log('🎵 Original playAudio function saved:', originals.playAudio);
    }} else {{
        console.warn('⚠️ No original playAudio function found at initialization');
    }}
        
    console.log('🎵 Crossfade: Saved originals');
    
    // 2. TEMPORARY WRAPPER - wird sofort aktiv
    window.playAudio = function(filepath, title, category) {{
        console.log('🎵 Crossfade: playAudio TEMPORARY WRAPPER called');
        console.log('🎵 Parameters:', {{ filepath: filepath, title: title, category: category }});
        
        // Check if plugin is ready
        if (window.CrossfadePlugin && window.CrossfadePlugin.handlePlayAudio) {{
            console.log('✅ Plugin ready, using plugin handler');
            return window.CrossfadePlugin.handlePlayAudio(filepath, title, category);
        }}
        
        // Plugin not ready yet, use original
        console.log('⚠️ Plugin not ready, using original function');
        
        // 🔧 KORREKTUR: Suche die ORIGINAL-FUNKTION (nicht die temporäre)
        let originalFunc = originals.playAudio;
        if (!originalFunc) {{
            // Versuche die Funktion aus dem globalen Scope zu finden
            if (window.originalPlayAudio) {{
                originalFunc = window.originalPlayAudio;
            }}
        }}
        
        if (originalFunc) {{
            console.log('🎵 Found original function, calling it');
            if (category !== undefined) {{
                return originalFunc(filepath, title, category);
            }}
            return originalFunc(filepath, title);
        }} else {{
            console.error('❌ No original playAudio function found!');
        }}
        
        return null;
    }};
    
    console.log('✅ playAudio temporarily wrapped');
    
    // 3. PLUGIN IMPLEMENTATION MIT LÖFFEL-SYSTEM
    const CrossfadePlugin = {{
        enabled: null,  // 🔧 Wird aus DOM geladen
        fadeDuration: null,  // 🔧 Wird aus DOM geladen
        fadeCurve: null,  // 🔧 Wird aus DOM geladen
        preloadNext: null,  // 🔧 Wird aus DOM geladen
        
        // 🥄 LÖFFEL-STATE: Nur EIN Player hat den Löffel!
        currentAudio: null,      // 🥄 Aktueller Löffel-Besitzer
        nextAudio: null,         // 🥄 Nächster in der Warteschlange
        isCrossfading: false,
        fadeStartTime: 0,
        nextTitle: null,
        baseVolume: 0.7,
        
        // UI Elements
        ui: {{}},
        
        // 🥄 Löffel-Übergabe-Log
        spoonLog: [],
        
        // Helper function to check autoplay
        isAutoplayEnabled: function() {{
            // 🔧 KORREKTUR 1: Direkter Check aus dem globalen State
            if (window.autoplayEnabled !== undefined) {{
                console.log('🥄 Autoplay from window.autoplayEnabled:', window.autoplayEnabled);
                return window.autoplayEnabled;
            }}
            
            // 🔧 KORREKTUR 2: Check aus Settings-Datenbank (wenn schon geladen)
            if (window.settings && window.settings.autoplay_enabled !== undefined) {{
                console.log('🥄 Autoplay from settings.autoplay_enabled:', window.settings.autoplay_enabled);
                return window.settings.autoplay_enabled;
            }}
            
            // 🔧 KORREKTUR 3: DOM-Element direkt prüfen
            const autoplaySetting = document.getElementById('autoplaySetting');
            if (autoplaySetting) {{
                const value = autoplaySetting.value === 'true';
                console.log('🥄 Autoplay from DOM element:', value);
                return value;
            }}
            
            // 🔧 KORREKTUR 4: DEFAULT = TRUE (weil Plugin sonst nicht funktioniert!)
            console.log('🥄 Autoplay DEFAULT (no data): true');
            return true;  // ✅ WICHTIG: Default auf true für Plugin-Funktionalität
        }},

        // 🥄 Löffel-Übergabe protokollieren
        logSpoonTransfer: function(from, to, action) {{
            const logEntry = {{
                time: new Date().toLocaleTimeString(),
                from: from,
                to: to,
                action: action,
                hasSpoon: this.currentAudio ? '🥄' : '❌'
            }};
            
            this.spoonLog.push(logEntry);
            
            // Keep only last 10 entries
            if (this.spoonLog.length > 10) {{
                this.spoonLog.shift();
            }}
            
            console.log(`🥄 LÖFFEL: ${{from}} → ${{to}} (${{action}})`);
            console.log(`   Aktueller Löffel-Besitzer: ${{this.currentAudio ? '🥄 Player ' + this.getPlayerId(this.currentAudio) : 'KEINER'}}`);
        }},
        
        // Player-ID für Debugging
        getPlayerId: function(audio) {{
            if (!audio) return 'none';
            return audio.src ? audio.src.substring(0, 30) + '...' : 'no-src';
        }},
        
        // Helper to get next track from current queue
        getNextTrackInQueue: function() {{
            console.log('🎵 Crossfade: getNextTrackInQueue called');
            
            if (!window.currentMediaQueue || window.currentMediaQueue.length === 0) {{
                console.log('🎵 Crossfade: No media queue, trying to create from DOM');
                if (!this.updateMediaQueueFromDOM()) {{
                    console.log('🎵 Crossfade: Could not create queue');
                    return null;
                }}
            }}
            
            if (window.currentMediaIndex === undefined || window.currentMediaIndex < 0) {{
                if (window.currentMediaInfo && window.currentMediaQueue) {{
                    const currentIndex = window.currentMediaQueue.findIndex(item => {{
                        return item.filepath === window.currentMediaInfo.filepath || 
                               item.encodedFilepath === encodeURIComponent(window.currentMediaInfo.filepath);
                    }});
                    
                    if (currentIndex >= 0) {{
                        window.currentMediaIndex = currentIndex;
                    }}
                }}
                
                if (window.currentMediaIndex === undefined || window.currentMediaIndex < 0) {{
                    console.log('🎵 Crossfade: Still no valid media index');
                    return null;
                }}
            }}
            
            const nextIndex = window.currentMediaIndex + 1;
            
            if (nextIndex >= window.currentMediaQueue.length) {{
                console.log('🎵 Crossfade: No more tracks in queue');
                return null;
            }}
            
            const nextTrack = window.currentMediaQueue[nextIndex];
            console.log('🎵 Crossfade: Next track found:', nextTrack.filename);
            
            return nextTrack;
        }},

        // Update media queue from DOM (fallback)
        updateMediaQueueFromDOM: function() {{
            console.log('🎵 Crossfade: Updating media queue from DOM');
            
            try {{
                const mediaCards = document.querySelectorAll('.media-card');
                const queue = [];
                
                mediaCards.forEach((card, index) => {{
                    const encodedFilepath = card.dataset.filepath || '';
                    const filename = card.dataset.filename || '';
                    const category = card.dataset.category || '';
                    
                    if (encodedFilepath) {{
                        const decodedFilepath = decodeURIComponent(encodedFilepath);
                        queue.push({{
                            encodedFilepath: encodedFilepath,
                            filepath: decodedFilepath,
                            filename: filename,
                            category: category,
                            index: index
                        }});
                    }}
                }});
                
                if (queue.length > 0) {{
                    window.currentMediaQueue = queue;
                    console.log('🎵 Crossfade: Media queue updated from DOM:', queue.length, 'tracks');
                    return true;
                }}
            }} catch (error) {{
                console.error('🎵 Crossfade: Error updating queue from DOM:', error);
            }}
            
            console.log('🎵 Crossfade: Could not create queue from DOM');
            return false;
        }},
        
        // 🔧 NEUE FUNKTION: Einstellungen aus dem DOM laden
        loadSettingsFromDOM: function() {{
            try {{
                console.log('🥄 Loading settings from DOM...');
                
                // 1. Enabled checkbox
                const enabledCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.enabled"]');
                if (enabledCheckbox && enabledCheckbox.type === 'checkbox') {{
                    this.enabled = enabledCheckbox.checked;
                    console.log('🥄 Enabled from DOM:', this.enabled);
                }}
                
                // 2. Fade Duration slider
                const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
                if (durationSlider && durationSlider.type === 'range') {{
                    this.fadeDuration = parseFloat(durationSlider.value);
                    console.log('🥄 Fade Duration from DOM:', this.fadeDuration, 's');
                    
                    // 🔥 KRITISCH: Auch den Text-Display aktualisieren!
                    const durationDisplay = document.getElementById('crossfadeDurationValue');
                    if (durationDisplay) {{
                        durationDisplay.textContent = this.fadeDuration + 's';
                        console.log('🥄 ✅ Duration display updated to:', this.fadeDuration + 's');
                    }}
                }}
                
                // 3. Fade Curve select
                const curveSelect = document.querySelector('[data-plugin-setting="plugin.crossfade.curve"]');
                if (curveSelect && curveSelect.tagName === 'SELECT') {{
                    this.fadeCurve = curveSelect.value;
                    console.log('🥄 Fade Curve from DOM:', this.fadeCurve);
                }}
                
                // 4. Preload checkbox
                const preloadCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.preload"]');
                if (preloadCheckbox && preloadCheckbox.type === 'checkbox') {{
                    this.preloadNext = preloadCheckbox.checked;
                    console.log('🥄 Preload from DOM:', this.preloadNext);
                }}
                
                console.log('🥄 Final settings loaded from DOM:', {{
                    enabled: this.enabled,
                    fadeDuration: this.fadeDuration,
                    fadeCurve: this.fadeCurve,
                    preloadNext: this.preloadNext
                }});
                
            }} catch (error) {{
                console.error('🥄 Error loading settings from DOM:', error);
            }}
        }},

        // 🔧 Settings nach dem Laden aktualisieren (OHNE Hook zu stören!)
        reloadSettingsFromDOM: function() {{
            console.log('🥄 Reloading settings from DOM (post-load)...');
            
            const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
            const enabledCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.enabled"]');
            const curveSelect = document.querySelector('[data-plugin-setting="plugin.crossfade.curve"]');
            const preloadCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.preload"]');
            
            if (durationSlider) {{
                this.fadeDuration = parseFloat(durationSlider.value);
                console.log('🥄 ✅ Updated fadeDuration:', this.fadeDuration);
            }}
            if (enabledCheckbox) {{
                this.enabled = enabledCheckbox.checked;
            }}
            if (curveSelect) {{
                this.fadeCurve = curveSelect.value;
            }}
            if (preloadCheckbox) {{
                this.preloadNext = preloadCheckbox.checked;
            }}
            
            console.log('🥄 Settings reloaded:', {{
                enabled: this.enabled,
                fadeDuration: this.fadeDuration,
                fadeCurve: this.fadeCurve,
                preloadNext: this.preloadNext
            }});
        }},
        
        // Initialize
        initialize: function() {{
            console.log('🎵 Crossfade: Initializing LÖFFEL-SYSTEM...');

            // 🔧 KORREKTUR: EINSTELLUNGEN DYNAMISCH AUS DEM UI LADEN!
            this.loadSettingsFromDOM();
            
            // Fallbacks setzen falls DOM leer war
            if (this.enabled === null) this.enabled = {str(self.enabled).lower()};
            if (this.fadeDuration === null) this.fadeDuration = {self.fade_duration};
            if (this.fadeCurve === null) this.fadeCurve = "{self.fade_curve}";
            if (this.preloadNext === null) this.preloadNext = {str(self.preload_next).lower()};
            
            console.log('🥄 Final settings after init:', {{
                enabled: this.enabled,
                fadeDuration: this.fadeDuration,
                fadeCurve: this.fadeCurve,
                preloadNext: this.preloadNext
            }});
            
            try {{
                // Find UI elements
                this.ui.titleElement = document.getElementById('playerTitle');
                this.ui.playBtnIcon = document.getElementById('playBtnIcon');
                this.ui.progressBar = document.getElementById('progressBar');
                this.ui.playerTime = document.getElementById('playerTime');
                this.ui.audioPlayer = document.getElementById('audioPlayer');
                this.ui.volumeControl = document.getElementById('volumeControl');
                this.ui.progressContainer = document.querySelector('.player-progress');
                
                console.log('🎵 Crossfade: UI elements found');
                console.log('🎵 Crossfade: Settings:', {{
                    enabled: this.enabled,
                    fadeDuration: this.fadeDuration,
                    fadeCurve: this.fadeCurve,
                    preloadNext: this.preloadNext
                }});
                
                // Setup event listeners
                if (this.ui.progressContainer) {{
                    this.ui.progressContainer.addEventListener('click', this.handleSeek.bind(this));
                }}
                
                if (this.ui.volumeControl) {{
                    this.ui.volumeControl.addEventListener('input', (e) => {{
                        this.baseVolume = parseFloat(e.target.value);
                        if (this.currentAudio && !this.isCrossfading) {{
                            this.currentAudio.volume = this.baseVolume;
                        }}
                    }});
                }}
                
                // Override other functions - OHNE originals-Check!
                console.log('🥄 Overriding togglePlay...');
                const self = this;
                window.togglePlay = function() {{
                    console.log('🥄 togglePlay wrapper called');
                    self.handleTogglePlay();
                }};
                console.log('🥄 ✅ togglePlay overridden');

                console.log('🥄 Overriding closeAudioPlayer...');
                window.closeAudioPlayer = function() {{
                    console.log('🥄 closeAudioPlayer wrapper called');
                    self.handleCloseAudioPlayer();
                }};
                console.log('🥄 ✅ closeAudioPlayer overridden');

                if (originals.seekAudio) {{
                    window.seekAudio = this.handleSeek.bind(this);
                }}

                if (originals.playNextMedia) {{
                    window.playNextMedia = this.handlePlayNextMedia.bind(this);
                }}
                
                console.log('🎵 Crossfade: ✅ LÖFFEL-SYSTEM initialized');
                console.log('🥄 Regel aktiv: Immer nur EIN Player hat den Löffel!');
                
                // Check autoplay status
                console.log('🎵 Crossfade: Autoplay enabled:', this.isAutoplayEnabled());
                
            }} catch (error) {{
                console.error('🎵 Crossfade: ❌ Initialization error:', error);
            }}
        }},
        
        // 🥄 Haupt-Löffel-Übergabe Funktion
        handlePlayAudio: function(filepath, title, category) {{
            console.log('🎵 Crossfade: 🎵🎵🎵 PLAY AUDIO - LÖFFEL-ÜBERGABE 🎵🎵🎵');
            console.log('🎵 Crossfade: Title:', title);
            console.log('🎵 Crossfade: Plugin enabled:', this.enabled);
            
            if (!this.enabled) {{
                console.log('🎵 Crossfade: Plugin disabled, using original function');
                
                // 🔧 KORREKTUR: ZURÜCK ZUM ORIGINAL MIT ALLEN PARAMETERN
                if (originals.playAudio) {{
                    // Stelle sicher, dass currentMediaInfo gesetzt ist
                    const trackCategory = category || 'Musik';
                    window.currentMediaInfo = {{
                        filepath: filepath,
                        filename: title,
                        category: trackCategory
                    }};
                    
                    console.log('🎵 Crossfade: Calling original playAudio with category:', trackCategory);
                    
                    // 🔥 WICHTIG: Alle Parameter korrekt übergeben
                    if (category !== undefined) {{
                        return originals.playAudio(filepath, title, category);
                    }}
                    return originals.playAudio(filepath, title);
                }} else {{
                    console.error('🎵 Crossfade: Original playAudio not found!');
                }}
                return null;
            }}
            
            // Plugin ist aktiviert - normal weiter
            console.log('🎵 Crossfade: Plugin enabled, using LÖFFEL-SYSTEM');
            
            // Update volume
            if (window.getCurrentVolume) {{
                this.baseVolume = window.getCurrentVolume();
            }}
            
            // Set current media info
            const trackCategory = category || (window.currentMediaInfo ? window.currentMediaInfo.category : 'Musik');
            
            if (window.currentMediaInfo === undefined) window.currentMediaInfo = {{}};
            window.currentMediaInfo = {{
                filepath: filepath,
                filename: title,
                category: trackCategory
            }};
            
            // 🥄 WICHTIG: Alten Löffel-Besitzer komplett stoppen
            if (this.currentAudio) {{
                console.log('🥄 Stoppe vorherigen Löffel-Besitzer...');
                
                // 🔧 KORREKTUR:
                const oldSpoonOwner = this.currentAudio;
                this.completelyStopAudio(oldSpoonOwner);
                
                // 🎯 DIESE EINE ZEILE FEHLTE:
                if (this.currentAudio === oldSpoonOwner) {{
                    this.currentAudio = null;
                }}
                
                this.logSpoonTransfer('OLD Player', 'NEW Player', 'MANUAL SWITCH');
            }}
            
            const safePath = encodeURIComponent(filepath);
            const audioElement = new Audio('/media?filepath=' + safePath);
            
            // 🥄 Neuer Löffel-Besitzer
            this.currentAudio = audioElement;
            this.logSpoonTransfer('NONE', 'NEW Player', 'INITIAL GRAB');
            
            // Setze currentMediaQueue wenn nicht vorhanden
            if (!window.currentMediaQueue || window.currentMediaQueue.length === 0) {{
                this.updateMediaQueueFromDOM();
            }}
            
            // Setze currentMediaIndex
            if (window.currentMediaQueue && window.currentMediaQueue.length > 0) {{
                const encodedFilepath = encodeURIComponent(filepath);
                const currentIndex = window.currentMediaQueue.findIndex(item => {{
                    return item.filepath === filepath || item.encodedFilepath === encodedFilepath;
                }});
                
                if (currentIndex >= 0) {{
                    window.currentMediaIndex = currentIndex;
                }}
            }}
            
            // Update UI
            if (this.ui.audioPlayer) {{
                this.ui.audioPlayer.style.display = 'block';
            }}
            if (this.ui.titleElement) {{
                this.ui.titleElement.textContent = title;
            }}
            if (this.ui.volumeControl) {{
                this.ui.volumeControl.value = this.baseVolume;
            }}
            
            // 🔧 KORREKTUR: Beim ERSTEN Start ist currentAudio null, also kein Crossfade
            // Aber: Autoplay trotzdem für ZUKÜNFTIGE Crossfades aktivieren!
            const isAutoplayTransition = this.currentAudio && 
                                       !this.currentAudio.paused && 
                                       !this.isCrossfading &&
                                       this.isAutoplayEnabled();

            console.log('🥄 Crossfade-Check:', {{
                hasSpoon: !!this.currentAudio,
                spoonOwner: this.getPlayerId(this.currentAudio),
                isAutoplayTransition: isAutoplayTransition,
                autoplayEnabled: this.isAutoplayEnabled(),
                firstTrack: !this.currentAudio  // 🔧 NEU: Erkenne ersten Track
            }});

            // 🔧 WICHTIG: Starte Player immer, aber merke dass Autoplay aktiv ist
            this.startSinglePlayer(audioElement, title);

            // 🔧 KORREKTUR: Speichere Autoplay-Status für ZUKÜNFTIGE Crossfades
            if (this.isAutoplayEnabled()) {{
                console.log('🥄 Autoplay aktiviert für zukünftige Crossfades');
                // Der timeupdate-Listener wird automatisch Crossfades triggern!
            }}
            
            return audioElement;
        }},
        
        // 🥄 KOMPLETTES STOPPEN eines Audio-Elements (Löffel abgeben)
        completelyStopAudio: function(audioElement) {{
            if (!audioElement) return;
            
            console.log(`🥄 Sanftes Stoppen von Player: ${{this.getPlayerId(audioElement)}}`);
            
            // 🔧 KORREKTUR: NUR PAUSIEREN, NICHT DIE QUELLE ZERSTÖREN!
            // 1. Pausieren (das genügt!)
            audioElement.pause();
            
            // 2. 🔧 KEIN src = '' MEHR! (lässt Hook leben)
            // audioElement.src = '';  // ❌ ENTFERNT!
            
            // 3. 🔧 KEIN load() MEHR! (verursacht Invalid State Error)
            // try {{
            //     audioElement.load();
            // }} catch (e) {{}}
            
            // 4. 🔧 EINFACH NUR CURRENTTIME ZURÜCKSETZEN
            audioElement.currentTime = 0;
            
            // 5. 🔧 VOLUME AUF 0 (verhindert Rest-Geräusche)
            audioElement.volume = 0;
            
            console.log(`🥄 Player ${{this.getPlayerId(audioElement)}} hat Löffel sanft abgegeben (Hook lebt!)`);
        }},
        
        saveCurrentHistory: function() {{
            if (this.currentAudio && window.currentMediaInfo && originals.addToHistory) {{
                const duration = parseFloat(this.currentAudio.duration);
                const position = parseFloat(this.currentAudio.currentTime);
                
                if (!isNaN(duration) && !isNaN(position) && duration > 0) {{
                    originals.addToHistory(
                        window.currentMediaInfo.filepath,
                        window.currentMediaInfo.filename,
                        window.currentMediaInfo.category,
                        position,
                        duration,
                        position >= duration
                    );
                }}
            }}
        }},

        // 🥄 NEUE FUNKTION: Hook-Listener an Player anbringen (wiederverwendbar!)
        attachSpoonHooks: function(audioElement) {{
            console.log('🥄 Attaching spoon hooks to player:', this.getPlayerId(audioElement));
            
            // 🥄 WICHTIGSTER LISTENER: Timeupdate für Crossfade-Trigger
            audioElement.addEventListener('timeupdate', () => {{
                this.updateProgress();
                
                // 🔧 DEBUG: Zeige DETAILLIERTEN Status
                const autoplayStatus = this.isAutoplayEnabled();
                const timeLeft = audioElement.duration - audioElement.currentTime;
                
                if (timeLeft <= this.fadeDuration + 10) {{
                    console.log('🥄 DETAILED Crossfade-Check:', {{
                        autoplay: autoplayStatus,
                        timeLeft: timeLeft.toFixed(1) + 's',
                        fadeDuration: this.fadeDuration + 's',
                        enabled: this.enabled,
                        isCrossfading: this.isCrossfading,
                        isCurrentAudio: this.currentAudio === audioElement,
                        durationValid: audioElement.duration > 0,
                        shouldTrigger: (this.enabled && 
                                      !this.isCrossfading && 
                                      this.currentAudio === audioElement &&
                                      autoplayStatus &&
                                      audioElement.duration > 0 &&
                                      timeLeft > 0 && 
                                      timeLeft <= this.fadeDuration + 0.5)
                    }});
                }}
                
                // 🥄 Crossfade-Zeit prüfen
                if (this.enabled && 
                    !this.isCrossfading && 
                    this.currentAudio === audioElement &&
                    autoplayStatus &&
                    audioElement.duration > 0) {{
                    
                    if (timeLeft > 0 && timeLeft <= this.fadeDuration + 0.5) {{
                        console.log('🥄 🔥 Crossfade time reached:', timeLeft.toFixed(1) + 's left');
                        this.loadNextTrackForCrossfade();
                    }}
                }}
            }});

            // Ended listener MIT KORREKTUR
            audioElement.addEventListener('ended', () => {{
                console.log('🥄 Track ended');
                
                // 🔧 KORREKTUR: Player gibt Löffel zurück wenn er endet
                if (this.currentAudio === audioElement) {{
                    console.log('🥄 🔄 Player ended - spoon released');
                    this.currentAudio = null;
                }}
                
                // Autoplay if no crossfade was triggered
                if (!this.isCrossfading && this.isAutoplayEnabled()) {{
                    console.log('🥄 Track ended, starting next track...');
                    setTimeout(() => this.handlePlayNextMedia(), 1000);
                }}
            }});
            
            console.log('🥄 ✅ Spoon hooks attached!');
        }},
        
        startSinglePlayer: function(audioElement, title) {{
            console.log('🥄 Starte Single Player:', title);
            
            audioElement.volume = this.baseVolume;

            // Metadata listener
            audioElement.addEventListener('loadedmetadata', () => {{
                console.log('🥄 METADATA loaded for', title, 
                    'duration:', audioElement.duration.toFixed(1) + 's');
                
                if (this.ui.playerTime) {{
                    const current = this.formatTime(audioElement.currentTime);
                    const duration = this.formatTime(audioElement.duration);
                    this.ui.playerTime.textContent = `${{current}} / ${{duration}}`;
                }}
            }});

            // Error listener
            audioElement.addEventListener('error', (e) => {{
                console.error('🥄 ERROR loading', title, 
                    'error:', audioElement.error);
            }});
            
            // 🥄 ALLE HOOK-LISTENER über neue Funktion anbringen
            this.attachSpoonHooks(audioElement);

            // Play!
            audioElement.play().then(() => {{
                console.log('🥄 ✅ Playback started - Löffel aktiv!');
                
                if (this.ui.playBtnIcon) {{
                    this.ui.playBtnIcon.className = 'fas fa-pause';
                }}
                
                // 🥄 UI Updates starten
                this.startUIUpdates();
                
            }}).catch(e => {{
                console.error('🥄 Playback error:', e);
            }});
        }},
        
        // 🥄 Nächsten Track für Crossfade laden
                loadNextTrackForCrossfade: function() {{
                    console.log('🥄 loadNextTrackForCrossfade called');
                    
                    // 🥄 CRITICAL CHECK 1: Schon im Crossfade?
                    if (this.isCrossfading) {{
                        console.log('🥄 ❌ Already crossfading, skipping');
                        return;
                    }}
                    
                    // 🥄 CRITICAL CHECK 2: Schon einen nächsten Player vorbereitet?
                    if (this.nextAudio) {{
                        console.log('🥄 ❌ Next audio already prepared, skipping');
                        return;
                    }}
                    
                    // 🥄 CRITICAL CHECK 3: Aktueller Player hat überhaupt den Löffel?
                    if (!this.currentAudio || this.currentAudio.paused) {{
                        console.log('🥄 ❌ Current audio not playing (no spoon), skipping crossfade');
                        return;
                    }}
                    
                    console.log('🥄 Loading next track for crossfade...');
                    
                    const autoplayEnabled = this.isAutoplayEnabled();
                    console.log('🥄 Autoplay status:', autoplayEnabled);
                    
                    if (!autoplayEnabled) {{
                        console.log('🥄 Autoplay disabled, skipping');
                        return;
                    }}
                    
                    // 🔧 KORREKTUR: Index VOR dem Suchen erhöhen!
                    console.log('🥄 Current media index BEFORE:', window.currentMediaIndex);
                    
                    // Nächsten Track finden
                    let next = null;
                    
                    if (originals.getNextMediaInQueue) {{
                        next = originals.getNextMediaInQueue();
                    }} else {{
                        next = this.getNextTrackInQueue();
                    }}
                    
                    if (next) {{
                        console.log('🥄 Next track found:', next.filename);
                        
                        // 🔧 WICHTIG: Index JETZT erhöhen, damit beim nächsten Crossfade der übernächste Track gefunden wird!
                        if (window.currentMediaQueue && window.currentMediaIndex !== undefined) {{
                            const nextIndex = window.currentMediaIndex + 1;
                            if (nextIndex < window.currentMediaQueue.length) {{
                                window.currentMediaIndex = nextIndex;
                                console.log('🥄 ✅ Media index advanced to:', window.currentMediaIndex);
                            }}
                        }}
                        
                        const nextPath = encodeURIComponent(next.filepath);
                        const nextAudio = new Audio('/media?filepath=' + nextPath);
                        nextAudio.volume = 0;
                        
                        // Metadaten listener
                        nextAudio.addEventListener('loadedmetadata', () => {{
                            console.log('🥄 Next track metadata loaded:', 
                                next.filename, nextAudio.duration.toFixed(1) + 's');
                        }});
                        
                        // 🔧 KORREKTUR: currentMediaInfo ERST nach Crossfade updaten!
                        // Sonst wird der aktuelle Track überschrieben bevor er fertig ist!
                        
                        // 🥄 Crossfade vorbereiten
                        this.prepareCrossfade(nextAudio, next.filename, next.filepath, next.category);
                        setTimeout(() => this.startCrossfade(), 100);
                    }} else {{
                        console.log('🥄 No next track available for crossfade');
                    }}
                }},
        
        // 🥄 Crossfade vorbereiten
                prepareCrossfade: function(nextAudio, title, filepath, category) {{
                    console.log('🥄 Preparing crossfade to:', title);
                    
                    // 🥄 Sicherstellen dass kein anderer "next" existiert
                    if (this.nextAudio) {{
                        console.log('🥄 ❌ Clearing existing next audio first');
                        this.completelyStopAudio(this.nextAudio);
                        this.nextAudio = null;
                    }}
                    
                    this.nextAudio = nextAudio;
                    this.nextTitle = title;
                    
                    // 🔧 NEU: Track-Info für späteren Update speichern
                    this.nextTrackInfo = {{
                        filepath: filepath,
                        filename: title,
                        category: category || 'Musik'
                    }};
                    
                    this.nextAudio.volume = 0;
                    
                    if (this.preloadNext) {{
                        this.nextAudio.load();
                    }}
                    
                    console.log('🥄 Next player prepared (waiting for spoon)');
                }},
        
        // 🥄 CROSSFADE STARTEN - LÖFFEL-ÜBERGABE!
        startCrossfade: function() {{
            if (!this.currentAudio || !this.nextAudio || this.isCrossfading) {{
                console.log('🥄 ❌ Cannot start crossfade - missing spoon or already fading');
                return;
            }}
            
            console.log('🥄 🥄🥄🥄 STARTING CROSSFADE - LÖFFEL-ÜBERGABE! 🥄🥄🥄');
            console.log('🥄 From:', this.ui.titleElement ? this.ui.titleElement.textContent : 'Unknown');
            console.log('🥄 To:', this.nextTitle);
            
            this.isCrossfading = true;
            this.fadeStartTime = Date.now();
            this.nextAudio.currentTime = 0;
            
            // 🥄 Protokolliere die Löffel-Übergabe
            this.logSpoonTransfer('Player ' + this.getPlayerId(this.currentAudio), 
                                'Player ' + this.getPlayerId(this.nextAudio), 
                                'CROSSFADE START');
            
            this.nextAudio.play().then(() => {{
                console.log('🥄 ✅ Next track playback started - Löffel wird übergeben');
                this.performFade();
            }}).catch(e => {{
                console.error('🥄 Crossfade play error:', e);
                this.isCrossfading = false;
            }});
        }},
        
        // 🥄 Fade ausführen
        performFade: function() {{
            if (!this.isCrossfading) return;
            
            const elapsed = (Date.now() - this.fadeStartTime) / 1000;
            const progress = Math.min(elapsed / this.fadeDuration, 1);
            
            let fadeOut = 1 - progress;
            let fadeIn = progress;
            
            if (this.fadeCurve === 'exponential') {{
                fadeOut = Math.pow(1 - progress, 2);
                fadeIn = Math.pow(progress, 2);
            }} else if (this.fadeCurve === 'logarithmic') {{
                fadeOut = Math.log10(1 + (1 - progress) * 9);
                fadeIn = Math.log10(1 + progress * 9);
            }}
            
            if (this.currentAudio) {{
                this.currentAudio.volume = Math.max(0, Math.min(1, fadeOut * this.baseVolume));
            }}
            if (this.nextAudio) {{
                this.nextAudio.volume = Math.max(0, Math.min(1, fadeIn * this.baseVolume));
            }}
            
            // Log fade progress
            if (Math.floor(elapsed * 10) % 5 === 0) {{
                console.log('🥄 Fade progress:', {{
                    elapsed: elapsed.toFixed(1) + 's',
                    progress: (progress * 100).toFixed(0) + '%',
                    currentVolume: (fadeOut * 100).toFixed(0) + '%',
                    nextVolume: (fadeIn * 100).toFixed(0) + '%'
                }});
            }}
            
            if (progress >= 1) {{
                this.completeCrossfade();
            }} else {{
                requestAnimationFrame(this.performFade.bind(this));
            }}
        }},
        
        // 🥄 CROSSFADE COMPLETE - LÖFFEL WIRD ÜBERGEBEN!
        completeCrossfade: function() {{
            console.log('🥄 ✅✅✅ CROSSFADE COMPLETE - LÖFFEL-ÜBERGABE! ✅✅✅');
            
            // 🔧 KORREKTUR: SANFTE LÖFFEL-ÜBERGABE
            if (this.currentAudio) {{
                console.log(`🥄 Sanfte Löffel-Übergabe von: ${{this.getPlayerId(this.currentAudio)}}`);
                
                // 🔧 NUR DAS, WAS WIRKLICH NOTWENDIG IST:
                this.currentAudio.pause();
                this.currentAudio.currentTime = 0;
                this.currentAudio.volume = 0;
            }}
            
            // 🥄 NEUER LÖFFEL-BESITZER
            const newOwner = this.nextAudio;
            this.currentAudio = newOwner;
            this.nextAudio = null;
            this.isCrossfading = false;
            
            if (this.currentAudio) {{
                this.currentAudio.volume = this.baseVolume;
                
                // 🔧 KRITISCH: currentMediaInfo JETZT updaten (nicht vorher!)
                if (this.nextTrackInfo) {{
                    window.currentMediaInfo = this.nextTrackInfo;
                    console.log('🥄 ✅ Updated currentMediaInfo:', window.currentMediaInfo.filename);
                    this.nextTrackInfo = null;
                }}
                
                // 🥄 **KRITISCH**: Neuer Besitzer braucht HOOK-LISTENER!
                this.attachSpoonHooks(this.currentAudio);
                
                // 🥄 UI für neuen Löffel-Besitzer aktualisieren
                if (this.ui.playerTime && this.currentAudio.duration > 0) {{
                    const current = this.formatTime(this.currentAudio.currentTime);
                    const duration = this.formatTime(this.currentAudio.duration);
                    this.ui.playerTime.textContent = `${{current}} / ${{duration}}`;
                }}
            }}
            
            if (this.nextTitle && this.ui.titleElement) {{
                this.ui.titleElement.textContent = this.nextTitle;
                this.nextTitle = null;
            }}
            
            console.log('🥄 Löffel-Übergabe abgeschlossen - Hook aktiv für neuen Besitzer!');
        }},
        
        // 🥄 UI für neuen Löffel-Besitzer aktualisieren
        updateUIForNewSpoonOwner: function() {{
            if (!this.currentAudio || !this.ui.playerTime) return;
            
            // Sofortige Aktualisierung
            const updateDisplay = () => {{
                if (this.currentAudio && this.currentAudio.duration > 0) {{
                    const current = this.formatTime(this.currentAudio.currentTime);
                    const duration = this.formatTime(this.currentAudio.duration);
                    this.ui.playerTime.textContent = `${{current}} / ${{duration}}`;
                    
                    // Fortschrittsbalken
                    if (this.ui.progressBar) {{
                        const progress = (this.currentAudio.currentTime / this.currentAudio.duration) * 100 || 0;
                        this.ui.progressBar.style.width = `${{progress}}%`;
                    }}
                }}
            }};
            
            updateDisplay();
            
            // Regelmäßige Updates starten
            this.startUIUpdates();
            
            console.log('🥄 UI updated for new spoon owner');
        }},
        
        // 🥄 UI Updates starten/stoppen
        startUIUpdates: function() {{
            // Altes Interval stoppen
            if (this.uiUpdateInterval) {{
                clearInterval(this.uiUpdateInterval);
            }}
            
            // Neues Interval starten
            this.uiUpdateInterval = setInterval(() => {{
                if (this.currentAudio && !this.currentAudio.paused) {{
                    if (this.ui.playerTime && this.currentAudio.duration > 0) {{
                        const current = this.formatTime(this.currentAudio.currentTime);
                        const duration = this.formatTime(this.currentAudio.duration);
                        this.ui.playerTime.textContent = `${{current}} / ${{duration}}`;
                    }}
                    
                    if (this.ui.progressBar && this.currentAudio.duration > 0) {{
                        const progress = (this.currentAudio.currentTime / this.currentAudio.duration) * 100 || 0;
                        this.ui.progressBar.style.width = `${{progress}}%`;
                    }}
                }}
            }}, 250);
        }},
        
        stopUIUpdates: function() {{
            if (this.uiUpdateInterval) {{
                clearInterval(this.uiUpdateInterval);
                this.uiUpdateInterval = null;
            }}
        }},
        
        handleTogglePlay: function() {{
            if (!this.currentAudio) return;
            
            if (this.isCrossfading) {{
                console.log('🥄 Crossfade in progress, cannot pause');
                return;
            }}
            
            if (this.currentAudio.paused) {{
                this.currentAudio.play();
                if (this.ui.playBtnIcon) {{
                    this.ui.playBtnIcon.className = 'fas fa-pause';
                }}
                this.startUIUpdates();
            }} else {{
                this.currentAudio.pause();
                if (this.ui.playBtnIcon) {{
                    this.ui.playBtnIcon.className = 'fas fa-play';
                }}
                this.stopUIUpdates();
            }}
        }},
        
    // 🥄 AUDIO PLAYER SCHLIESSEN - ALLE LÖFFEL ABGEBEN!
        handleCloseAudioPlayer: function() {{
            console.log('🥄 🛑 CLOSING PLAYER - Stopping ALL audio');
            
            // 1. UI Updates sofort stoppen
            this.stopUIUpdates();
            
            // 2. Crossfade-Flag setzen
            this.isCrossfading = false;
            
            // 3. ALLE Audio-Elemente finden und BRUTAL stoppen
            const audioToStop = [];
            if (this.currentAudio) audioToStop.push(this.currentAudio);
            if (this.nextAudio) audioToStop.push(this.nextAudio);
            
            console.log('🥄 Stopping', audioToStop.length, 'audio elements');
            
            audioToStop.forEach((audio, i) => {{
                if (audio) {{
                    console.log(`🥄 Stopping audio ${{i + 1}}`);
                    try {{
                        audio.pause();
                        audio.volume = 0;
                        audio.currentTime = 0;
                        // BEIM SCHLIESSEN dürfen wir brutal sein:
                        audio.src = '';
                        audio.load();
                    }} catch (e) {{
                        console.log('🥄 Stop error (ignored):', e);
                    }}
                }}
            }});
            
            // 4. State zurücksetzen
            this.currentAudio = null;
            this.nextAudio = null;
            this.nextTitle = null;
            this.isCrossfading = false;
            
            // 5. UI zurücksetzen
            if (this.ui.audioPlayer) {{
                this.ui.audioPlayer.style.display = 'none';
            }}
            if (this.ui.playBtnIcon) {{
                this.ui.playBtnIcon.className = 'fas fa-play';
            }}
            if (this.ui.progressBar) {{
                this.ui.progressBar.style.width = '0%';
            }}
            if (this.ui.playerTime) {{
                this.ui.playerTime.textContent = '00:00 / 00:00';
            }}
            
            console.log('🥄 ✅ Player closed, all audio stopped');
        }},
        
        handleSeek: function(event) {{
            if (!this.currentAudio || !this.ui.progressContainer) return;
            
            const rect = this.ui.progressContainer.getBoundingClientRect();
            const pos = (event.clientX - rect.left) / rect.width;
            
            if (pos >= 0 && pos <= 1) {{
                const newTime = pos * this.currentAudio.duration;
                this.currentAudio.currentTime = newTime;
                console.log('🥄 Seek to:', Math.round(newTime) + 's');
            }}
        }},
        
        handlePlayNextMedia: function() {{
            console.log('🥄 Play next media called');
            
            if (!this.isAutoplayEnabled()) {{
                console.log('🥄 Autoplay disabled, skipping');
                return;
            }}
            
            // Nächsten Track finden
            let next = null;
            
            if (originals.getNextMediaInQueue) {{
                next = originals.getNextMediaInQueue();
            }} else {{
                next = this.getNextTrackInQueue();
            }}
            
            if (next) {{
                console.log('🥄 Playing next track:', next.filename);
                this.handlePlayAudio(next.filepath, next.filename, next.category);
            }} else {{
                console.log('🥄 No next track available');
            }}
        }},
        
        updateProgress: function() {{
            if (!this.currentAudio || !this.ui.progressBar) return;
            
            const progress = (this.currentAudio.currentTime / this.currentAudio.duration) * 100 || 0;
            this.ui.progressBar.style.width = progress + '%';
        }},
        
        // Helper: Format seconds to MM:SS or HH:MM:SS
        formatTime: function(seconds) {{
            if (!seconds || isNaN(seconds)) return '00:00';
            const hours = Math.floor(seconds / 3600);
            const mins = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {{
                return `${{hours.toString().padStart(2, '0')}}:${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }} else {{
                return `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}
        }},
        
        // Settings update
        updateSettings: function(settings) {{
            console.log('🥄 Updating settings:', settings);
            
            if (settings.enabled !== undefined) this.enabled = settings.enabled;
            
            if (settings.fadeDuration !== undefined) {{
                this.fadeDuration = parseFloat(settings.fadeDuration);
                console.log('🥄 Updated fadeDuration to:', this.fadeDuration);
                
                // 🔧 UI auch updaten!
                const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
                const durationDisplay = document.getElementById('crossfadeDurationValue');
                
                if (durationSlider) {{
                    durationSlider.value = this.fadeDuration;
                }}
                if (durationDisplay) {{
                    durationDisplay.textContent = this.fadeDuration + 's';
                    console.log('🥄 ✅ Duration display updated to:', this.fadeDuration + 's');
                }}
            }}
            
            if (settings.fadeCurve !== undefined) this.fadeCurve = settings.fadeCurve;
            if (settings.preloadNext !== undefined) this.preloadNext = settings.preloadNext;
            
            console.log('🥄 ✅ Settings updated:', {{
                enabled: this.enabled,
                fadeDuration: this.fadeDuration,
                fadeCurve: this.fadeCurve,
                preloadNext: this.preloadNext
            }});
            
            // 🔧 WICHTIG: AUCH DAS DOM-UI AKTUALISIEREN
            this.updateDOMSettings();
            
            console.log('🥄 ✅ Settings updated successfully');
        }},
        
        // 🔧 NEUE FUNKTION: DOM-UI mit aktuellen Werten aktualisieren
        updateDOMSettings: function() {{
            try {{
                // Duration slider
                const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
                if (durationSlider && durationSlider.type === 'range') {{
                    durationSlider.value = this.fadeDuration;
                    const valueDisplay = document.getElementById('crossfadeDurationValue');
                    if (valueDisplay) {{
                        valueDisplay.textContent = this.fadeDuration + 's';
                    }}
                }}
                
                // Curve select
                const curveSelect = document.querySelector('[data-plugin-setting="plugin.crossfade.curve"]');
                if (curveSelect && curveSelect.tagName === 'SELECT') {{
                    curveSelect.value = this.fadeCurve;
                }}
                
                // Enabled checkbox
                const enabledCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.enabled"]');
                if (enabledCheckbox && enabledCheckbox.type === 'checkbox') {{
                    enabledCheckbox.checked = this.enabled;
                }}
                
                // Preload checkbox
                const preloadCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.preload"]');
                if (preloadCheckbox && preloadCheckbox.type === 'checkbox') {{
                    preloadCheckbox.checked = this.preloadNext;
                }}
                
                // Status-Anzeige aktualisieren
                const statusElement = document.getElementById('crossfadeStatus');
                if (statusElement) {{
                    statusElement.textContent = this.enabled ? "Aktiv 🥄" : "Inaktiv ❌";
                    statusElement.style.color = this.enabled ? "#2ecc71" : "#e74c3c";
                }}
                
                console.log('🥄 DOM UI updated with current settings');
            }} catch (error) {{
                console.error('🥄 Error updating DOM:', error);
            }}
        }}
    }};
    
    // 4. MAKE PLUGIN AVAILABLE
    window.CrossfadePlugin = CrossfadePlugin;
    console.log('✅ CrossfadePlugin object created with LÖFFEL-SYSTEM');
    
    // 5. SETTINGS INTEGRATION
    if (!window.collectPluginSettings) window.collectPluginSettings = function() {{ return {{}}; }};
    if (!window.applyPluginSettings) window.applyPluginSettings = function() {{}};
    
    const originalCollectSettings = window.collectPluginSettings;
    window.collectPluginSettings = function() {{
        const settings = originalCollectSettings();
        if (window.CrossfadePlugin) {{
            settings['plugin.crossfade.enabled'] = window.CrossfadePlugin.enabled;
            settings['plugin.crossfade.duration'] = window.CrossfadePlugin.fadeDuration;
            settings['plugin.crossfade.curve'] = window.CrossfadePlugin.fadeCurve;
            settings['plugin.crossfade.preload'] = window.CrossfadePlugin.preloadNext;
        }}
        return settings;
    }};
    
    const originalApplySettings = window.applyPluginSettings;
    window.applyPluginSettings = function(settings) {{
        if (originalApplySettings) originalApplySettings(settings);
        
        console.log('🥄 applyPluginSettings called with:', settings);
        
        if (settings && window.CrossfadePlugin && window.CrossfadePlugin.updateSettings) {{
            // 🔧 KORREKTUR: Settings richtig extrahieren
            const crossfadeSettings = {{
                enabled: settings['plugin.crossfade.enabled'] !== undefined 
                        ? settings['plugin.crossfade.enabled'] 
                        : window.CrossfadePlugin.enabled,
                fadeDuration: settings['plugin.crossfade.duration'] !== undefined
                             ? parseFloat(settings['plugin.crossfade.duration'])
                             : window.CrossfadePlugin.fadeDuration,
                fadeCurve: settings['plugin.crossfade.curve'] !== undefined
                          ? settings['plugin.crossfade.curve']
                          : window.CrossfadePlugin.fadeCurve,
                preloadNext: settings['plugin.crossfade.preload'] !== undefined
                            ? settings['plugin.crossfade.preload']
                            : window.CrossfadePlugin.preloadNext
            }};
            
            console.log('🥄 Applying crossfade settings:', crossfadeSettings);
            window.CrossfadePlugin.updateSettings(crossfadeSettings);
        }}
    }};
    
    console.log('✅ Settings integration ready');
    
    // 6. INITIALIZE - SOFORT!
    console.log('🥄 Checking document state:', document.readyState);

    function initialize() {{
        console.log('🥄 🔥 INITIALIZE CALLED!');
        if (window.CrossfadePlugin) {{
            window.CrossfadePlugin.initialize();
            
            // Replace temporary wrapper with real handler
            window.playAudio = function(filepath, title, category) {{
                return window.CrossfadePlugin.handlePlayAudio(filepath, title, category);
            }};
            
            console.log('✅ playAudio wrapper replaced');
        }} else {{
            console.log('❌ CrossfadePlugin not found!');
        }}
    }}

    // SOFORT ausführen wenn DOM ready
    if (document.readyState === 'loading') {{
        console.log('🥄 Document loading, waiting for DOMContentLoaded');
        document.addEventListener('DOMContentLoaded', () => {{
            console.log('🥄 DOMContentLoaded fired');
            initialize();
        }});
    }} else {{
        console.log('🥄 Document already ready, initializing now');
        initialize();
    }}

    // Fallback
    setTimeout(() => {{
        console.log('🥄 Fallback initialization check');
        if (!window.CrossfadePlugin || !window.CrossfadePlugin.ui.titleElement) {{
            console.log('🥄 Fallback: Re-initializing');
            initialize();
        }}
    }}, 500);
    
}})();

console.log('✅ {self.name} v{self.version}: LÖFFEL-SYSTEM fully loaded!');
console.log('🥄 MERKE: Immer nur EIN Löffel, immer weitergeben!');

// 🔥 SOFORT INITIALISIEREN - NICHT WARTEN!
console.log('🥄 Starting immediate initialization...');
if (window.CrossfadePlugin) {{
    console.log('🥄 CrossfadePlugin found, calling initialize()');
    window.CrossfadePlugin.initialize();
    
    // playAudio override
    window.playAudio = function(filepath, title, category) {{
        return window.CrossfadePlugin.handlePlayAudio(filepath, title, category);
    }};
    console.log('🥄 ✅ Functions overridden');
}} else {{
    console.log('🥄 ❌ CrossfadePlugin NOT FOUND!');
}}
</script>'''
        
        return js_code
    
    def get_settings_html(self):
        """HTML für Plugin-Einstellungen."""
        enabled_checked = "checked" if self.enabled else ""
        preload_checked = "checked" if self.preload_next else ""
        
        html = f'''
    <div class="plugin-settings" data-plugin="{self.name}">
        <h4><i class="fas fa-wave-square"></i> Crossfade Plugin v{self.version} 🥄</h4>
        <div class="settings-group">
            <label class="settings-label">
                <input type="checkbox" data-plugin-setting="plugin.crossfade.enabled" {enabled_checked}>
                Crossfade aktivieren
            </label>
            <small class="text-muted">Nahtlose Überblendung zwischen Audio-Tracks</small>
        </div>
        <div class="settings-group">
            <label class="settings-label">Überblend-Dauer: <span id="crossfadeDurationValue"></span></label>
            <input type="range" data-plugin-setting="plugin.crossfade.duration" 
                   class="settings-slider" min="1" max="10" step="0.5" 
                   value="{self.fade_duration}" 
                   oninput="document.getElementById('crossfadeDurationValue').textContent = this.value + 's'">
            <small class="text-muted">Länge der Überblendung zwischen Tracks (1-10 Sekunden)</small>
        </div>
        <div class="settings-group">
            <label class="settings-label">Fade-Kurve:</label>
            <select data-plugin-setting="plugin.crossfade.curve" class="settings-select">
                <option value="linear" {"selected" if self.fade_curve == "linear" else ""}>Linear (gleichmäßig)</option>
                <option value="exponential" {"selected" if self.fade_curve == "exponential" else ""}>Exponentiell (sanft)</option>
                <option value="logarithmic" {"selected" if self.fade_curve == "logarithmic" else ""}>Logarithmisch (dynamisch)</option>
            </select>
            <small class="text-muted">Art der Überblendung</small>
        </div>
        <div class="settings-group">
            <label class="settings-label">
                <input type="checkbox" data-plugin-setting="plugin.crossfade.preload" {preload_checked}>
                Nächstes Audio vorladen
            </label>
            <small class="text-muted">Bessere Performance bei schnellen Übergängen</small>
        </div>
        <div class="plugin-status" style="margin-top: 10px; padding: 8px; background: rgba(0,0,0,0.1); border-radius: 4px;">
            <small>
                <i class="fas fa-info-circle"></i> 
                <strong>🥄 LÖFFEL-SYSTEM:</strong> Immer nur EIN Player aktiv<br>
                Status: <span id="crossfadeStatus" style="font-weight: bold; color: {"#2ecc71" if self.enabled else "#e74c3c"}">{"Aktiv 🥄" if self.enabled else "Inaktiv ❌"}</span> | 
                Dauer: <span id="currentFadeDuration">{self.fade_duration}</span>s | 
                Kurve: <span id="currentFadeCurve">{self.fade_curve}</span>
            </small>
        </div>
        <script>
        // 🔧 LIVE-UPDATE für die Status-Anzeige
        function updateCrossfadeStatus() {{
            console.log('🥄 updateCrossfadeStatus() called');
            const enabledCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.enabled"]');
            const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
            const curveSelect = document.querySelector('[data-plugin-setting="plugin.crossfade.curve"]');
            
            console.log('🥄 Slider value:', durationSlider ? durationSlider.value : 'NOT FOUND');
            
            if (enabledCheckbox && durationSlider && curveSelect) {{
                const status = document.getElementById('crossfadeStatus');
                const currentDuration = document.getElementById('currentFadeDuration');
                const currentCurve = document.getElementById('currentFadeCurve');
                
                if (status) {{
                    status.textContent = enabledCheckbox.checked ? "Aktiv 🥄" : "Inaktiv ❌";
                    status.style.color = enabledCheckbox.checked ? "#2ecc71" : "#e74c3c";
                }}
                if (currentDuration) {{
                    currentDuration.textContent = durationSlider.value;
                }}
                if (currentCurve) {{
                    currentCurve.textContent = curveSelect.options[curveSelect.selectedIndex].text;
                }}
                
                // 🔥 KRITISCH: Auch den Haupttext beim Slider aktualisieren!
                const durationDisplay = document.getElementById('crossfadeDurationValue');
                if (durationDisplay) {{
                    durationDisplay.textContent = durationSlider.value + 's';
                }}
            }}
        }}
        
        // Event-Listener für Live-Updates
        document.addEventListener('DOMContentLoaded', function() {{
            const enabledCheckbox = document.querySelector('[data-plugin-setting="plugin.crossfade.enabled"]');
            const durationSlider = document.querySelector('[data-plugin-setting="plugin.crossfade.duration"]');
            const curveSelect = document.querySelector('[data-plugin-setting="plugin.crossfade.curve"]');
            
            if (enabledCheckbox) {{
                enabledCheckbox.addEventListener('change', updateCrossfadeStatus);
            }}
            if (durationSlider) {{
                durationSlider.addEventListener('input', updateCrossfadeStatus);
            }}
            if (curveSelect) {{
                curveSelect.addEventListener('change', updateCrossfadeStatus);
            }}
        }});
        
        // 🔥 NEU: Warte auf Settings-Laden, DANN update
        window.addEventListener('settingsLoaded', function() {{
            console.log('🥄 settingsLoaded event received, updating status');
                
            // 🔥 WICHTIG: Settings im Plugin-Objekt aktualisieren!
            if (window.CrossfadePlugin && window.CrossfadePlugin.reloadSettingsFromDOM) {{
                    window.CrossfadePlugin.reloadSettingsFromDOM();
            }}
                
            // DANN das UI aktualisieren
            updateCrossfadeStatus();
        }});
            
        // 🔥 FALLBACK: Falls kein Event kommt, nach 500ms trotzdem updaten
        setTimeout(function() {{
            console.log('🥄 Fallback update after 500ms');
                
            // 🔥 WICHTIG: Settings im Plugin-Objekt aktualisieren!
            if (window.CrossfadePlugin && window.CrossfadePlugin.reloadSettingsFromDOM) {{
                window.CrossfadePlugin.reloadSettingsFromDOM();
            }}
                
            // DANN das UI aktualisieren
            updateCrossfadeStatus();
        }}, 500);
    </script>
    </div>
    '''
        
        return html
    
    def save_settings(self):
        """Plugin Settings speichern."""
        return {
            'plugin.crossfade.enabled': bool(self.enabled),
            'plugin.crossfade.duration': float(self.fade_duration),
            'plugin.crossfade.curve': str(self.fade_curve),
            'plugin.crossfade.preload': bool(self.preload_next),
            'plugin.crossfade.version': str(self.version)
        }

Plugin = CrossfadePlugin
