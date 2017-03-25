/*
 * Author: Ameya Raje
 * Student ID: 54729960
 * 
 * 
 * HW1: Q3
 */


import java.io.*;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.*;

public class TotalFreq {
	
	static HashMap<String, Integer> result = new HashMap<>();
	static FileInputStream input = null;
	static Scanner sc = null;
	
	public static void main(String[] args) throws Exception {
		
		long start =  System.nanoTime();
		
		result = tokenize(args[0]);
		result = tokenize(args[1]);
		sortAndPrint(result);
		
		long end = System.nanoTime();
		long diff = end-start;
		long msTime = diff/1000000;
		System.out.println("Time taken to execute is : " + msTime + " ms");
		
	}
	
	public static HashMap<String, Integer> tokenize(String filePath) throws Exception {
		
		try {
			input = new FileInputStream(filePath);
			sc = new Scanner(input);
			while (sc.hasNextLine()) {
				String line = sc.nextLine();
				line = line.toLowerCase();

				String[] tokens = line.split(",");

				if (tokens.length != 2)
					continue;

				String word = tokens[0];
				int freq = Integer.parseInt(tokens[1]);

				if (!result.containsKey(word))
					result.put(word, freq);
				else
					result.put(word, result.get(word)+freq);
			}

//					for (String s: result.keySet()) {
//						
//						System.out.println("Tokens " + s + " Freq " + result.get(s));
//					}

		}
		catch(Exception e) {
			e.getMessage();
		}
		finally {
			sc.close();
			input.close();
		}
		return result;
	}

	public static void sortAndPrint(HashMap<String, Integer> map) {
		Set<Map.Entry<String,Integer>> set = map.entrySet();
		List<Map.Entry<String, Integer>> list = new ArrayList<Map.Entry<String, Integer>>(set);
		Collections.sort(list, (o1, o2) -> (o1.getKey()).compareTo(o2.getKey()));
		PrintWriter writer = null;
		
		try {
			writer = new PrintWriter("output.txt", "UTF-8");
			for (Map.Entry<String, Integer> entry:list) {
	            writer.println("Token: " + entry.getKey()+" Freq: "+entry.getValue());
	        }
		}
		catch(Exception e) {
			e.getMessage();
		}
		finally {
			writer.close();
		}
		
//		for (Map.Entry<String, Integer> entry:list) {
//            System.out.println("Token: " + entry.getKey()+" Freq: "+entry.getValue());
//        }
		
	}
}