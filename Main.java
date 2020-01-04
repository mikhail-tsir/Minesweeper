import java.awt.*;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;

import javax.swing.*;

public class Main extends JFrame implements KeyListener {

	public static char direction = 'l';
	JLabel[][] snakeArray = new JLabel[30][30];
	public Main(String s) {
		super(s);
		addKeyListener(this);
		
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Main frame = new Main("Snake game");
		JLabel[][] snakeArray = new JLabel[30][30];
		JPanel myPanel = new JPanel();
		myPanel.setLayout(null);
		myPanel.setVisible(true);
		myPanel.setSize(450,450);
		
		for (int row = 0; row < snakeArray.length; row++) {
			for (int col = 0; col < snakeArray[row].length; col++) {
				snakeArray[row][col] = new JLabel();
				snakeArray[row][col].setSize(new Dimension(15,15));
				snakeArray[row][col].setBackground(new Color(50,180,255));
				snakeArray[row][col].setLocation(row * 15, col * 15);
				snakeArray[row][col].setVisible(true);
				snakeArray[row][col].setOpaque(true);
				myPanel.add(snakeArray[row][col]);
			}
		}
		
		
		frame.getContentPane().add(myPanel);
		frame.setSize(500, 500);
		frame.setVisible(true);
		
		int headX = (int)(Math.random()*30);
		int headY = (int)(Math.random()*30);
		
		JLabel head = snakeArray[headX][headY];
		head.setBackground(new Color(9,42,200));
		
		ArrayList<JLabel> tail = new ArrayList<JLabel>();
		
		for (JLabel t : tail) {
			t.setBackground(new Color(55,55,55));
		}
		
		
		int foodX = 0;
		int foodY = 0;
		
		do {
			foodX = (int)(Math.random() * 30);
			foodY = (int)(Math.random() * 30);
		} while (tail.contains(snakeArray[foodX][foodY]));
		
		JLabel food = snakeArray[foodX][foodY];
		
		food.setBackground(new Color(255,0,100));
		
		while (true) {
			int wait = 175;
			long time = System.currentTimeMillis() + wait;
			
			head.setBackground(new Color(9,42,200));
			food.setBackground(new Color(255,0,100));
			
			ArrayList<JLabel> tempTail = new ArrayList<JLabel>();
			
			for (int i = 0; i < tail.size(); i++) {
				tempTail.add(tail.get(i));
			}
			
			if (tail.size() > 0) {
				tail.set(0,snakeArray[headX][headY]);
			}
			
			JLabel tempHead = snakeArray[headX][headY];
			
			if (direction == 'l') {
				headX--;
			} else if (direction == 'r') {
				headX++;
			} else if (direction == 'u') {
				headY--;
			} else if (direction == 'd') {
				headY++;
			}
			
			System.out.println("(" + headX + ", " + headY + ")");
			
			if ((direction == 'l' && headX == 0)
					|| (direction == 'r' && headX == 29)
					|| (direction == 'u' && headY == 0)
					|| (direction == 'd' && headY == 29)){
				wait = 300;
			}
			
			
			if (headX == -1 || headY == -1 || headX == 30 || headY == 30) {
				System.out.println("SCORE: " + tail.size());
				System.exit(0);
			}
			
			for (int i = 1; i < tail.size(); i++) {
				tail.set(i, tempTail.get(i-1));
			}
			
			head = snakeArray[headX][headY];
			
			if (tail.contains(head) && tail.size() >= 1) {
				System.out.println("SCORE: " + tail.size());
				System.exit(0);
			}
			
			
			
			while (System.currentTimeMillis() < time) {
				//do nothing
			}
			
			if (wait == 300) {
				wait = 175;
			}
			
			/*for (JLabel[] array : snakeArray) {
				for (JLabel label : array) {
					label.setBackground(new Color(50,180,255));
				}
			}*/
			
			if (tempTail.size() > 0) {
				tempTail.get(tempTail.size() -1).setBackground(new Color(50,180,255));
			} else {
				tempHead.setBackground(new Color(50,180,255));
			}
			
			
			
			for (JLabel t : tail) {
				t.setBackground(new Color(55,55,55));
			}
			
			head.setBackground(new Color(9,42,200));
			food.setBackground(new Color(255,0,100));
			
			if (foodX == headX && foodY == headY) {
				
				if (tail.size() == 0) {
					tail.add(head);
				} else {
					tail.add(tail.size() -1, tail.get(tail.size()-1));
				}
				
				do {
					foodX = (int)(Math.random() * 30);
					foodY = (int)(Math.random() * 30);
				} while (tail.contains(snakeArray[foodX][foodY]));
				
				food = snakeArray[foodX][foodY];
				food.setBackground(new Color(255,0,100));
				
			}
			
		}
	}

	@Override
	public void keyPressed(KeyEvent arg0) {
		switch (arg0.getKeyCode()) {
		case KeyEvent.VK_UP: if (direction != 'd') direction = 'u'; break;
		case KeyEvent.VK_DOWN: if (direction != 'u') direction = 'd'; break;
		case KeyEvent.VK_LEFT: if (direction != 'r') direction = 'l'; break;
		case KeyEvent.VK_RIGHT: if (direction != 'l') direction = 'r'; break;
		default: direction = 'u'; break;
		}
		
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

}
