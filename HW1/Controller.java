/*
 * Author: Ameya Raje
 * Student ID: 54729960
 * 
 * 
 * HW1: Q1
 */

import java.util.*;
import java.util.Map.Entry;
import java.io.*;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public class Controller {

	public static void main(String[] args) throws Exception {
		
		long start =  System.nanoTime();
		
		HashMap<String, Integer> result = new HashMap<String, Integer>();
		result = tokenize(args[0]);
		
		printTokens(result);
		
		long end = System.nanoTime();
		long diff = end-start;
		long msTime = diff/1000000;
		System.out.println("Time taken to execute is : " + msTime + " ms");
		
	}
	
	public static HashMap<String, Integer> tokenize(String filePath) throws Exception {
		
		FileInputStream input = null;
		Scanner sc = null;
		HashMap<String, Integer> freqCount = new HashMap<String, Integer>();
		
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

					if (isAlpha || isNumber) {
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
						if (freqCount.containsKey(word))
							freqCount.put(word, freqCount.get(word)+1);
						else
							freqCount.put(word,1);
						start = -1;
						end = -1;
					}	
				}
			}
			
			Set<Map.Entry<String,Integer>> set = freqCount.entrySet();
			List<Map.Entry<String, Integer>> list = new ArrayList<Map.Entry<String, Integer>>(set);
			Collections.sort(list, (o1, o2) -> (o2.getValue()).compareTo( o1.getValue() ));
			
			for (Map.Entry<String, Integer> entry:list) {
	            System.out.println("Token: " + entry.getKey()+" Freq: "+entry.getValue());
	        }
			
		}
		catch(Exception e) {
			e.getMessage();
		}
		finally {
			input.close();
			sc.close();

		}
		return freqCount;
	}	
	
	public static void printFreq(HashMap<String, Integer> map) {
		System.out.println("----------------\nFrequencies are\n");
		
		Set<Map.Entry<String,Integer>> set = map.entrySet();
		List<Map.Entry<String, Integer>> list = new ArrayList<Map.Entry<String, Integer>>(set);
		Collections.sort( list, (o1, o2) -> (o2.getValue()).compareTo( o1.getValue() ));
		for(Map.Entry<String, Integer> entry:list){
            System.out.println("Token: " + entry.getKey()+" Freq: "+entry.getValue());
        }
		System.out.println("----------------");
	}
	
	public static void printTokens(HashMap<String, Integer> map) {
		System.out.println("----------------\nTokens are\n");
		for (String s: map.keySet()) {
			System.out.println(s);
		}
		System.out.println("----------------");
	}
}
