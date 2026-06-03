"""Real-time input polling system for Hole Wizards."""

import sys
import time


class RealtimeInput:
    """Handles keyboard input polling for real-time mode."""
    
    def __init__(self):
        """Initialize the input system."""
        self.input_buffer = []
        self.platform = sys.platform
        self._setup_platform_specific()
    
    def _setup_platform_specific(self):
        """Set up platform-specific input handling."""
        if self.platform.startswith('win'):
            self._setup_windows()
        else:
            self._setup_unix()
    
    def _setup_windows(self):
        """Set up Windows input handling using msvcrt."""
        try:
            import msvcrt
            self.msvcrt = msvcrt
            self.platform_input = self._poll_windows
        except ImportError:
            self.platform_input = self._poll_fallback
    
    def _setup_unix(self):
        """Set up Unix/Linux/macOS input handling using termios."""
        try:
            import tty
            import termios
            self.tty = tty
            self.termios = termios
            self.platform_input = self._poll_unix
            # Store original terminal settings
            self.original_settings = termios.tcgetattr(sys.stdin)
        except ImportError:
            self.platform_input = self._poll_fallback
    
    def _poll_windows(self):
        """Poll for input on Windows."""
        keys_pressed = []
        while self.msvcrt.kbhit():
            char = self.msvcrt.getch()
            # Handle special keys
            if char == b'\xe0':  # Arrow keys prefix
                char = self.msvcrt.getch()
                if char == b'H':
                    keys_pressed.append('w')  # Up arrow
                elif char == b'P':
                    keys_pressed.append('s')  # Down arrow
                elif char == b'K':
                    keys_pressed.append('a')  # Left arrow
                elif char == b'M':
                    keys_pressed.append('d')  # Right arrow
            else:
                try:
                    keys_pressed.append(char.decode('utf-8').lower())
                except:
                    pass
        return keys_pressed
    
    def _poll_unix(self):
        """Poll for input on Unix-like systems."""
        import select
        keys_pressed = []
        
        # Check if input is available (non-blocking)
        if select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            
            # Handle escape sequences (arrow keys)
            if char == '\x1b':
                # Check for more characters in escape sequence
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    char2 = sys.stdin.read(1)
                    if char2 == '[':
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            char3 = sys.stdin.read(1)
                            if char3 == 'A':
                                keys_pressed.append('w')  # Up arrow
                            elif char3 == 'B':
                                keys_pressed.append('s')  # Down arrow
                            elif char3 == 'C':
                                keys_pressed.append('d')  # Right arrow
                            elif char3 == 'D':
                                keys_pressed.append('a')  # Left arrow
            else:
                keys_pressed.append(char.lower())
        
        return keys_pressed
    
    def _poll_fallback(self):
        """Fallback input polling (blocking, not ideal for real-time)."""
        return []
    
    def poll_keys(self):
        """Poll for currently pressed keys.
        
        Returns:
            list: List of key characters pressed this frame
        """
        return self.platform_input()
    
    def enter_realtime_mode(self):
        """Enter real-time mode (set terminal to raw mode on Unix)."""
        if self.platform.startswith('win'):
            return
        
        try:
            # Set terminal to raw mode for character-by-character input
            self.tty.setcbreak(sys.stdin.fileno())
        except:
            pass
    
    def exit_realtime_mode(self):
        """Exit real-time mode (restore terminal settings on Unix)."""
        if self.platform.startswith('win'):
            return
        
        try:
            # Restore original terminal settings
            self.termios.tcsetattr(sys.stdin, self.termios.TCSADRAIN, self.original_settings)
        except:
            pass
    
    def cleanup(self):
        """Clean up input system."""
        self.exit_realtime_mode()
