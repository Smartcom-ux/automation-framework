package listeners;
import org.testng.ITestListener;
import org.testng.ITestResult;

import util.ScreenshotUtil;
	
public class TestListener implements 	ITestListener{
	 @Override
	    public void onTestFailure(ITestResult result) {

	        ScreenshotUtil.capture(result.getName());
	    }
}
