import java.lang.Math.*;

public class ProgrammingChallenges
{

public static int getMaxexp(int k, int b)
  {
    int e = 0;
    int prev = 1;
    while(prev*b < k)
    {
      e++;
      prev = prev*b;
      }
    return e;

  }
public static String toString(int[] a)
{
  String s = " ";
  for(int i = 0; i < a.length; i++)
  {
    s = s + a[i];
  }
  return s;
}
public static int getMultiplicity(int k, int x)
{
  int temp = k;
  int count = 0;
  while(temp >= x)
  {
    count++;
    temp = temp - x;
  }
  return count;
}
public static int getinBase(int m, int b)
{
  int e = getMaxexp(m,b);
  int[] dig = new int[1000];
  int prev = m;
  int index = 0 ;
  while(e > 0)
  {
    int x = (int)Math.pow(b,e);
  int c =  getMultiplicity(prev,x);
  dig[index] = c;
  prev = prev - c*x;
  index++;
  e = getMaxexp(prev,b);
  }
  if(prev != 0 ){
  index++;
  dig[index] = prev;}
  int ind2 = 0;
  int convertedint = 0;
  boolean stop = false;
  while(ind2 <= index && !stop)
  {

    if(dig[ind2]>=10)
    {stop = true;}
    convertedint = convertedint + dig[ind2]*(int)Math.pow(10,index - ind2);
    ind2++;
  }
  if(stop){convertedint = -1;}
  return convertedint;
}

public static void main(String[] args)
{
  System.out.println(getinBase(10000015,16));
}

}
