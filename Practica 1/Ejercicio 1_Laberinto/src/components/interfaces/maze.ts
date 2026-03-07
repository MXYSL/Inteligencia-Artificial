export interface MazeCell {
  x: number;      // Horizontal position, integer
  y: number;      // Vertical position, integer
  top: boolean;   // Top/Up has a wall/blocked if true, boolean
  left: boolean;  // Left has a wall/blocked if true, boolean
  bottom: boolean;// Bottom/Down has a wall/blocked if true, boolean
  right: boolean; // Right has a wall/blocked if true, boolean
  set: number;    // Used internally by the generation algorithm
}

