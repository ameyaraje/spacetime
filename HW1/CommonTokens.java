/*
 * Author: Ameya Raje
 * Student ID: 54729960
 * 
 * 
 * HW1: Q2
 */

import java.io.FileInputStream;
import java.io.InputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.*;

public class CommonTokens {
	
	public static void main(String[] args) throws Exception {
		
		long start =  System.nanoTime();
		
		HashSet<String> file1 = new HashSet<>();
		HashSet<String> file2 = new HashSet<>();
		
		file1 = tokenize(args[0]);
		file2 = tokenize(args[1]);
		getIntersection(file1, file2);
		
		long end = System.nanoTime();
		long diff = end-start;
		long msTime = diff/1000000;
		System.out.println("Time taken to execute is : " + msTime + " ms");
	}
	
	public static HashSet<String> tokenize(String filePath) throws Exception {

		InputStream input = new FileInputStream(filePath);
		HashSet<String> freqCount = new HashSet<String>();				
		Scanner sc = null;
		
		try {
			input = new FileInputStream(filePath);
			sc = new Scanner(input);
			while (sc.hasNextLine()) {

				String line = sc.nextLine();
				int start = -1;
				int end = -1;

				for (int i = 0; i < line.length(); i++) {
					char currChar = line.charAt(i);

					boolean isAlpha = Character.isDigit(currChar);
					boolean isNumber = Character.isDefined(currChar);

					if ((isAlpha || isNumber)) {
						if (start == -1) {
							start = i;
							end = i;
						}
						else
							end = i+1;
					}

					if (end == line.length() || (!Character.isAlphabetic(line.charAt(end))) && !Character.isDigit(line.charAt(end))) {
						if (start == end) {
							start = -1;
							end = -1;
							continue;
						}
						String word = line.substring(start, end);
						word = word.toLowerCase();
						if (!freqCount.contains(word))
							freqCount.add(word);
						start = -1;
						end = -1;
					}

				}

			}
		}
		catch(Exception e) {
			e.getMessage();
		}
		finally {

			sc.close();
			input.close();
		}
		return freqCount;
	}	
	
	
	public static void getIntersection(HashSet<String> file1, HashSet<String> file2) {
		int count = 0;
		
		System.out.println("-----------");
		System.out.println("The common tokens are - ");
		for (String s: file1) {
			if (file2.contains(s)) {
				System.out.println(s);
				count++;
			}
		}
		
		System.out.println("The number of common tokens is: " + count);
		System.out.println("-----------");
	}
}
