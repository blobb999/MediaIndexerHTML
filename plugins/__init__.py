# -*- coding: utf-8 -*-
"""
🧩 PLUGIN MANAGER für Media Platform - FUNKTIONIERT ÜBERALL
"""

import importlib
import os
import sys
import traceback

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.hooks = {}
        print("🧩 PluginManager initialisiert")
    
    def load_plugins(self):
        """Lädt alle Plugins - FUNKTIONIERT IN IDLE, EXE UND ENTWICKLUNG"""
        print("🔍 Suche Plugins...")
        
        # WICHTIG: Mehrere mögliche Plugin-Pfade
        possible_plugin_dirs = self._get_possible_plugin_dirs()
        
        plugins_found = 0
        for plugin_dir in possible_plugin_dirs:
            if os.path.exists(plugin_dir):
                print(f"✅ Plugin-Verzeichnis gefunden: {plugin_dir}")
                plugins_found += self._load_from_directory(plugin_dir)
        
        if plugins_found == 0:
            print("⚠️ Keine Plugins gefunden")
            print("ℹ️ Mögliche Plugin-Pfade:")
            for path in possible_plugin_dirs:
                print(f"   - {path}")
        
        print(f"✅ Plugin-Laden abgeschlossen: {len(self.plugins)} Plugin(s) geladen")
    
    def _get_possible_plugin_dirs(self):
        """Gibt alle möglichen Plugin-Verzeichnisse zurück"""
        possible_dirs = []
        
        # 1. PyInstaller EXE-Modus
        if getattr(sys, 'frozen', False):
            # EXE-Pfad Verzeichnis
            exe_dir = os.path.dirname(sys.executable)
            possible_dirs.append(os.path.join(exe_dir, 'plugins'))
            
            # Arbeitsverzeichnis
            possible_dirs.append(os.path.join(os.getcwd(), 'plugins'))
        
        # 2. Normales Python (IDLE, Terminal, etc.)
        else:
            # Versuche mehrere mögliche Pfade
            
            # A) Relativ zum aktuellen Skript
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                possible_dirs.append(script_dir)
            except:
                pass
            
            # B) Projektverzeichnis (wo media_platform.py ist)
            main_file = 'media_platform.py'
            if os.path.exists(main_file):
                project_dir = os.path.dirname(os.path.abspath(main_file))
                possible_dirs.append(os.path.join(project_dir, 'plugins'))
            
            # C) Arbeitsverzeichnis
            possible_dirs.append(os.path.join(os.getcwd(), 'plugins'))
            
            # D) Speziell für IDLE: Elternverzeichnis von __file__
            try:
                if __file__:
                    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    possible_dirs.append(os.path.join(parent_dir, 'plugins'))
            except:
                pass
        
        # Entferne Duplikate
        unique_dirs = []
        for d in possible_dirs:
            if d not in unique_dirs:
                unique_dirs.append(d)
        
        return unique_dirs
    
    def _load_from_directory(self, plugin_dir):
        """Lädt Plugins aus einem Verzeichnis - Gibt Anzahl geladener Plugins zurück"""
        loaded_count = 0
        
        if not os.path.exists(plugin_dir):
            return 0
        
        print(f"  🔎 Durchsuche: {plugin_dir}")
        
        for item in os.listdir(plugin_dir):
            plugin_path = os.path.join(plugin_dir, item)
            
            # Nur Verzeichnisse, keine __pycache__ etc.
            if not os.path.isdir(plugin_path):
                continue
                
            if (item.startswith('__') or 
                item.startswith('.') or
                item == '__pycache__'):
                continue
            
            print(f"    🔍 Prüfe Plugin-Ordner: {item}")
            
            # Prüfe ob Plugin-Datei existiert
            init_file = os.path.join(plugin_path, '__init__.py')
            if not os.path.exists(init_file):
                print(f"      ⚠️ Keine __init__.py gefunden, überspringe")
                continue
            
            try:
                success = self._load_plugin_from_path(item, plugin_path, init_file)
                if success:
                    loaded_count += 1
                    
            except Exception as e:
                print(f"      ❌ Plugin {item} Fehler: {e}")
                traceback.print_exc()
        
        return loaded_count
    
    def _load_plugin_from_path(self, plugin_name, plugin_path, init_file):
        """Lädt ein Plugin von einem bestimmten Pfad"""
        # WICHTIG: Verschiedene Import-Methoden basierend auf Kontext
        
        # 1. Versuche als Python-Modul zu importieren (normale Umgebung)
        try:
            # Füge Plugin-Pfad zu sys.path hinzu
            parent_dir = os.path.dirname(plugin_path)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            # Importiere das Modul
            if getattr(sys, 'frozen', False):
                # In EXE: importiere direkt aus Datei
                return self._load_plugin_direct(plugin_name, init_file)
            else:
                # Normal: Standard-Import
                return self._load_plugin_normal(plugin_name, parent_dir)
                
        except Exception as e:
            print(f"      ⚠️ Standard-Import fehlgeschlagen: {e}")
            
            # 2. Fallback: Importiere direkt aus Datei
            try:
                return self._load_plugin_direct(plugin_name, init_file)
            except Exception as e2:
                print(f"      ❌ Direkter Import auch fehlgeschlagen: {e2}")
                return False
    
    def _load_plugin_normal(self, plugin_name, parent_dir):
        """Lädt Plugin mit normalem Python-Import"""
        # Temporär sys.path ändern
        old_sys_path = sys.path.copy()
        try:
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            # Importiere das Modul
            module_name = plugin_name
            module = importlib.import_module(module_name)
            
            return self._create_plugin_instance(plugin_name, module)
            
        finally:
            # sys.path zurücksetzen
            sys.path = old_sys_path
    
    def _load_plugin_direct(self, plugin_name, init_file_path):
        """Lädt Plugin direkt aus Datei (funktioniert überall)"""
        import importlib.util
        
        try:
            # Erstelle einen eindeutigen Modulnamen
            module_name = f"plugin_{plugin_name}_{hash(init_file_path)}"
            
            # Lade Modul direkt aus Datei
            spec = importlib.util.spec_from_file_location(
                module_name, 
                init_file_path
            )
            
            if spec is None:
                print(f"      ❌ Kann Spec für {plugin_name} nicht erstellen")
                return False
            
            module = importlib.util.module_from_spec(spec)
            
            # Füge zum sys.modules hinzu
            sys.modules[module_name] = module
            
            # Führe das Modul aus
            spec.loader.exec_module(module)
            
            return self._create_plugin_instance(plugin_name, module)
            
        except Exception as e:
            print(f"      ❌ Direkter Import fehlgeschlagen: {e}")
            return False
    
    def _create_plugin_instance(self, plugin_name, module):
        """Erstellt eine Plugin-Instanz aus einem Modul"""
        try:
            # Prüfe ob Plugin-Klasse existiert
            if not hasattr(module, 'Plugin'):
                print(f"      ❌ Keine 'Plugin' Klasse in {plugin_name}")
                return False
            
            # Hole die Plugin-Klasse
            plugin_class = module.Plugin
            
            # Prüfe ob es eine Klasse ist
            if not isinstance(plugin_class, type):
                print(f"      ❌ 'Plugin' in {plugin_name} ist keine Klasse")
                return False
            
            # Instanz erstellen
            plugin_instance = plugin_class()
            self.plugins[plugin_name] = plugin_instance
            
            plugin_display_name = getattr(plugin_instance, 'name', plugin_name)
            print(f"      ✅ Plugin geladen: {plugin_display_name}")
            
            # Plugin registrieren lassen
            if hasattr(plugin_instance, 'register'):
                try:
                    success = plugin_instance.register(self)
                    if success:
                        print(f"      ✅ Plugin registriert")
                    else:
                        print(f"      ⚠️ Plugin-Registrierung fehlgeschlagen")
                except Exception as e:
                    print(f"      ⚠️ Register-Methode fehlgeschlagen: {e}")
            else:
                print(f"      ⚠️ Plugin hat keine register()-Methode")
            
            return True
            
        except Exception as e:
            print(f"      ❌ Fehler beim Erstellen der Plugin-Instanz: {e}")
            return False

    # ============================================================
    # REST DER METHODEN (UNVERÄNDERT)
    # ============================================================

    def save_plugin_settings(self):
        """Sammelt Settings von allen Plugins über den Hook-Mechanismus"""
        print("💾 Speichere alle Plugin-Settings...")
        
        # Alle save_settings Hooks triggern
        results = self.trigger_hook('settings.save')
        
        # Combine all results into a single dictionary
        all_settings = {}
        for plugin_settings in results:
            if isinstance(plugin_settings, dict):
                all_settings.update(plugin_settings)
        
        print(f"✅ Alle Plugin-Settings gesammelt: {len(all_settings)} Einträge")
        return all_settings

    def load_plugin_settings(self, settings_dict):
        """Lädt Settings für alle Plugins über den Hook-Mechanismus"""
        print("📥 Lade Plugin-Settings...")
        
        if not settings_dict:
            print("⚠️ Keine Settings zum Laden")
            return False
        
        # Alle load_settings Hooks triggern
        success_count = 0
        results = self.trigger_hook('settings.load', settings_dict)
        
        for result in results:
            if result:
                success_count += 1
        
        print(f"✅ Plugin-Settings geladen: {success_count}/{len(self.plugins)} Plugins")
        return success_count > 0
    
    def register_hook(self, hook_name, callback):
        """Plugin kann Hooks registrieren - MIT VALIDIERUNG"""
        if not callable(callback):
            print(f"⚠️ Hook '{hook_name}': Callback ist nicht aufrufbar")
            return False
        
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        # Verhindere doppelte Registrierung
        if callback not in self.hooks[hook_name]:
            self.hooks[hook_name].append(callback)
            print(f"✅ Hook registriert: '{hook_name}' für {callback.__module__}")
            return True
        else:
            print(f"⚠️ Hook '{hook_name}' bereits registriert")
            return False
    
    def trigger_hook(self, hook_name, *args, **kwargs):
        """Trigger alle Callbacks für einen Hook - MIT BESSERER FEHLERBEHANDLUNG FÜR SETTINGS"""
        results = []
        
        if hook_name not in self.hooks:
            # DEBUG: Welche Hooks sind verfügbar?
            if hook_name in ['html.header', 'html.settings', 'settings.save', 'settings.load']:
                print(f"🔍 Hook '{hook_name}' nicht registriert, verfügbare Hooks: {list(self.hooks.keys())}")
            return results
        
        callbacks = self.hooks.get(hook_name, [])
        print(f"🔌 Trigger Hook '{hook_name}' mit {len(callbacks)} Callback(s)")
        
        for i, callback in enumerate(callbacks):
            try:
                callback_name = callback.__name__ if hasattr(callback, '__name__') else str(callback)
                print(f"  🔧 Callback {i+1}: {callback_name}")
                
                # SPEZIALBEHANDLUNG FÜR SETTINGS.SAVE
                if hook_name == 'settings.save':
                    result = callback()  # Keine Parameter für save_settings
                elif hook_name == 'settings.load':
                    # settings.load bekommt das Settings-Dictionary als erstes Argument
                    result = callback(*args, **kwargs) if args or kwargs else callback()
                elif hook_name == 'html.header':
                    result = callback()
                elif hook_name == 'html.settings':
                    result = callback()
                elif hook_name.startswith('audio.'):
                    # Audio-Hooks mit Parametern
                    result = callback(*args, **kwargs) if args or kwargs else callback()
                else:
                    # Generischer Fall
                    result = callback(*args, **kwargs)
                
                if result is not None:
                    # Für settings.save: Prüfe ob es ein Dictionary ist
                    if hook_name == 'settings.save':
                        if isinstance(result, dict):
                            # Validierung: Alle Werte müssen serialisierbar sein
                            valid_result = {}
                            for k, v in result.items():
                                if isinstance(v, (bool, int, float, str, type(None))):
                                    valid_result[str(k)] = v
                                else:
                                    # Nicht-serialisierbar → String-Konvertierung
                                    valid_result[str(k)] = str(v)
                                    print(f"  ⚠️ Wert für {k} wurde zu String konvertiert: {type(v)}")
                            
                            if valid_result:
                                results.append(valid_result)
                                print(f"  ✅ Callback {i+1} erfolgreich, {len(valid_result)} Settings")
                            else:
                                print(f"  ⚠️ Callback {i+1} kein gültiges Dictionary")
                        else:
                            print(f"  ⚠️ Callback {i+1} hat kein Dictionary zurückgegeben: {type(result)}")
                    else:
                        results.append(result)
                        print(f"  ✅ Callback {i+1} erfolgreich, Ergebnis: {type(result).__name__}")
                else:
                    print(f"  ℹ️ Callback {i+1} kein Ergebnis")
                    
            except Exception as e:
                print(f"  ❌ Callback {i+1} Fehler: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"✅ Hook '{hook_name}' abgeschlossen: {len(results)} Ergebnisse")
        return results
    
    def get_all_settings_html(self):
        """Sammelt HTML von allen Plugins - MIT FEHLERHANDLING"""
        html_parts = []
        
        print(f"🔍 Sammle Settings HTML von {len(self.plugins)} Plugins")
        
        for plugin_name, plugin in self.plugins.items():
            print(f"  📝 Plugin: {plugin_name}")
            
            if hasattr(plugin, 'get_settings_html'):
                try:
                    html = plugin.get_settings_html()
                    if html and html.strip():
                        html_parts.append(html)
                        print(f"    ✅ HTML erhalten ({len(html)} Zeichen)")
                    else:
                        print(f"    ⚠️ Kein HTML oder leer")
                except Exception as e:
                    print(f"    ❌ HTML-Generierung fehlgeschlagen: {e}")
            else:
                print(f"    ℹ️ Keine get_settings_html() Methode")
        
        result = '\n'.join(html_parts)
        print(f"✅ Settings HTML gesammelt: {len(result)} Zeichen insgesamt")
        return result

# Singleton Plugin Manager Instanz
plugin_manager = PluginManager()
