import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Production CORS configuration
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
    # Production on Railway
    CORS(app, origins=[
        "https://*.vercel.app",  # Allow all Vercel deployments
        "https://buy-the-dip-beige.vercel.app",  # Replace with your specific Vercel URL
        "http://localhost:3000",  # For local development
        "http://127.0.0.1:5000"   # For local development
    ])
    print("🌍 Production CORS enabled for Vercel domains")
else:
    # Development
    CORS(app)
    print("🔧 Development CORS enabled for all origins")

# Comprehensive stock lists - manually curated and reliable
def get_nifty_50_stocks():
    """Nifty 50 stocks - most reliable large cap stocks"""
    return [
        {'symbol': 'ADANIENT.NS', 'name': 'Adani Enterprises', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports and Special Economic Zone', 'sector': 'infrastructure', 'marketCap': 'large'},
        {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals Enterprise', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BEL.NS', 'name': 'Bharat Electronics', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel', 'sector': 'telecom', 'marketCap': 'large'},
        {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'COALINDIA.NS', 'name': 'Coal India', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddy\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'ETERNAL.NS', 'name': 'Eternal', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life Insurance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ITC.NS', 'name': 'ITC', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'INFY.NS', 'name': 'Infosys', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'JIOFIN.NS', 'name': 'Jio Financial Services', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'sector': 'construction', 'marketCap': 'large'},
        {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'NTPC.NS', 'name': 'NTPC', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'ONGC.NS', 'name': 'Oil & Natural Gas Corporation', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corporation of India', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'SBILIFE.NS', 'name': 'SBI Life Insurance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'SHRIRAMFIN.NS', 'name': 'Shriram Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical Industries', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer Products', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'TITAN.NS', 'name': 'Titan Company', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'TRENT.NS', 'name': 'Trent', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'sector': 'it', 'marketCap': 'large'}
    ]

def get_nifty_100_stocks():
    """Nifty 100 stocks - includes Nifty 50 + Next 50"""
    return [
        {'symbol': 'ABB.NS', 'name': 'ABB India', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ADANIENSOL.NS', 'name': 'Adani Energy Solutions', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIENT.NS', 'name': 'Adani Enterprises', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'ADANIGREEN.NS', 'name': 'Adani Green Energy', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports and Special Economic Zone', 'sector': 'infrastructure', 'marketCap': 'large'},
        {'symbol': 'ADANIPOWER.NS', 'name': 'Adani Power', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'AMBUJACEM.NS', 'name': 'Ambuja Cements', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals Enterprise', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'DMART.NS', 'name': 'Avenue Supermarts', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJHLDNG.NS', 'name': 'Bajaj Holdings & Investment', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJHFL.NS', 'name': 'Bajaj Housing Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BANKBARODA.NS', 'name': 'Bank of Baroda', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BEL.NS', 'name': 'Bharat Electronics', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'BPCL.NS', 'name': 'Bharat Petroleum Corporation', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel', 'sector': 'telecom', 'marketCap': 'large'},
        {'symbol': 'BOSCHLTD.NS', 'name': 'Bosch', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BRITANNIA.NS', 'name': 'Britannia Industries', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'CGPOWER.NS', 'name': 'CG Power and Industrial Solutions', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'CANBK.NS', 'name': 'Canara Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'CHOLAFIN.NS', 'name': 'Cholamandalam Investment and Finance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'COALINDIA.NS', 'name': 'Coal India', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'DLF.NS', 'name': 'DLF', 'sector': 'realty', 'marketCap': 'large'},
        {'symbol': 'DABUR.NS', 'name': 'Dabur India', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'DIVISLAB.NS', 'name': 'Divi\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddy\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'ETERNAL.NS', 'name': 'Eternal', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'GAIL.NS', 'name': 'GAIL (India)', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'GODREJCP.NS', 'name': 'Godrej Consumer Products', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life Insurance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'HAVELLS.NS', 'name': 'Havells India', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'HAL.NS', 'name': 'Hindustan Aeronautics', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'HYUNDAI.NS', 'name': 'Hyundai Motor India', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ICICIGI.NS', 'name': 'ICICI Lombard General Insurance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ICICIPRULI.NS', 'name': 'ICICI Prudential Life Insurance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ITC.NS', 'name': 'ITC', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'INDHOTEL.NS', 'name': 'Indian Hotels Co.', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'IOC.NS', 'name': 'Indian Oil Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'IRFC.NS', 'name': 'Indian Railway Finance Corporation', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'NAUKRI.NS', 'name': 'Info Edge (India)', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'INFY.NS', 'name': 'Infosys', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'INDIGO.NS', 'name': 'InterGlobe Aviation', 'sector': 'infrastructure', 'marketCap': 'mid'},
        {'symbol': 'JSWENERGY.NS', 'name': 'JSW Energy', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'JINDALSTEL.NS', 'name': 'Jindal Steel & Power', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'JIOFIN.NS', 'name': 'Jio Financial Services', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'LTIM.NS', 'name': 'LTIMindtree', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'sector': 'construction', 'marketCap': 'mid'},
        {'symbol': 'LICI.NS', 'name': 'Life Insurance Corporation of India', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'LODHA.NS', 'name': 'Lodha Developers', 'sector': 'realty', 'marketCap': 'mid'},
        {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'NTPC.NS', 'name': 'NTPC', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'ONGC.NS', 'name': 'Oil & Natural Gas Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'PIDILITIND.NS', 'name': 'Pidilite Industries', 'sector': 'chemicals', 'marketCap': 'mid'},
        {'symbol': 'PFC.NS', 'name': 'Power Finance Corporation', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corporation of India', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'PNB.NS', 'name': 'Punjab National Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'RECLTD.NS', 'name': 'REC', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'SBILIFE.NS', 'name': 'SBI Life Insurance Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'MOTHERSON.NS', 'name': 'Samvardhana Motherson International', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'SHREECEM.NS', 'name': 'Shree Cement', 'sector': 'cement', 'marketCap': 'mid'},
        {'symbol': 'SHRIRAMFIN.NS', 'name': 'Shriram Finance', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'SIEMENS.NS', 'name': 'Siemens', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical Industries', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'SWIGGY.NS', 'name': 'Swiggy', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'TVSMOTOR.NS', 'name': 'TVS Motor Company', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer Products', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'TATAPOWER.NS', 'name': 'Tata Power Co.', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'TITAN.NS', 'name': 'Titan Company', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'TORNTPHARM.NS', 'name': 'Torrent Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'TRENT.NS', 'name': 'Trent', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement', 'sector': 'cement', 'marketCap': 'mid'},
        {'symbol': 'UNITDSPR.NS', 'name': 'United Spirits', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'VBL.NS', 'name': 'Varun Beverages', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'VEDL.NS', 'name': 'Vedanta', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'ZYDUSLIFE.NS', 'name': 'Zydus Lifesciences', 'sector': 'healthcare', 'marketCap': 'mid'}
    ]

def get_nifty_200_stocks():
    """Nifty 200 stocks - comprehensive list of top 200 Indian companies"""
    return [
        {'symbol': 'ABB.NS', 'name': 'ABB India', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ACC.NS', 'name': 'ACC', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'APLAPOLLO.NS', 'name': 'APL Apollo Tubes', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'AUBANK.NS', 'name': 'AU Small Finance Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ADANIENSOL.NS', 'name': 'Adani Energy Solutions', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIENT.NS', 'name': 'Adani Enterprises', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'ADANIGREEN.NS', 'name': 'Adani Green Energy', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports and Special Economic Zone', 'sector': 'infrastructure', 'marketCap': 'large'},
        {'symbol': 'ADANIPOWER.NS', 'name': 'Adani Power', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ATGL.NS', 'name': 'Adani Total Gas', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ABCAPITAL.NS', 'name': 'Aditya Birla Capital', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ABFRL.NS', 'name': 'Aditya Birla Fashion and Retail', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'ALKEM.NS', 'name': 'Alkem Laboratories', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'AMBUJACEM.NS', 'name': 'Ambuja Cements', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals Enterprise', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'APOLLOTYRE.NS', 'name': 'Apollo Tyres', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'ASHOKLEY.NS', 'name': 'Ashok Leyland', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'ASTRAL.NS', 'name': 'Astral', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'AUROPHARMA.NS', 'name': 'Aurobindo Pharma', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'DMART.NS', 'name': 'Avenue Supermarts', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BSE.NS', 'name': 'BSE', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJHLDNG.NS', 'name': 'Bajaj Holdings & Investment', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BAJAJHFL.NS', 'name': 'Bajaj Housing Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BANDHANBNK.NS', 'name': 'Bandhan Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BANKBARODA.NS', 'name': 'Bank of Baroda', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BANKINDIA.NS', 'name': 'Bank of India', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'MAHABANK.NS', 'name': 'Bank of Maharashtra', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'BDL.NS', 'name': 'Bharat Dynamics', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'BEL.NS', 'name': 'Bharat Electronics', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'BHARATFORG.NS', 'name': 'Bharat Forge', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BHEL.NS', 'name': 'Bharat Heavy Electricals', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'BPCL.NS', 'name': 'Bharat Petroleum Corporation', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel', 'sector': 'telecom', 'marketCap': 'large'},
        {'symbol': 'BHARTIHEXA.NS', 'name': 'Bharti Hexacom', 'sector': 'telecom', 'marketCap': 'large'},
        {'symbol': 'BIOCON.NS', 'name': 'Biocon', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'BOSCHLTD.NS', 'name': 'Bosch', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'BRITANNIA.NS', 'name': 'Britannia Industries', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'CGPOWER.NS', 'name': 'CG Power and Industrial Solutions', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'CANBK.NS', 'name': 'Canara Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'CHOLAFIN.NS', 'name': 'Cholamandalam Investment and Finance Company', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'COALINDIA.NS', 'name': 'Coal India', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'COCHINSHIP.NS', 'name': 'Cochin Shipyard', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'COFORGE.NS', 'name': 'Coforge', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'COLPAL.NS', 'name': 'Colgate Palmolive (India)', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'CONCOR.NS', 'name': 'Container Corporation of India', 'sector': 'infrastructure', 'marketCap': 'mid'},
        {'symbol': 'CUMMINSIND.NS', 'name': 'Cummins India', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'DLF.NS', 'name': 'DLF', 'sector': 'realty', 'marketCap': 'mid'},
        {'symbol': 'DABUR.NS', 'name': 'Dabur India', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'DIVISLAB.NS', 'name': 'Divi\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'DIXON.NS', 'name': 'Dixon Technologies (India)', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddy\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'ESCORTS.NS', 'name': 'Escorts Kubota', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'ETERNAL.NS', 'name': 'Eternal', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'EXIDEIND.NS', 'name': 'Exide Industries', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'NYKAA.NS', 'name': 'FSN E-Commerce Ventures', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'FEDERALBNK.NS', 'name': 'Federal Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'GAIL.NS', 'name': 'GAIL (India)', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'GMRAIRPORT.NS', 'name': 'GMR Airports', 'sector': 'infrastructure', 'marketCap': 'mid'},
        {'symbol': 'GLENMARK.NS', 'name': 'Glenmark Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'GODREJCP.NS', 'name': 'Godrej Consumer Products', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'GODREJPROP.NS', 'name': 'Godrej Properties', 'sector': 'realty', 'marketCap': 'mid'},
        {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries', 'sector': 'cement', 'marketCap': 'mid'},
        {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'HDFCAMC.NS', 'name': 'HDFC Asset Management Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life Insurance Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'HAVELLS.NS', 'name': 'Havells India', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'HAL.NS', 'name': 'Hindustan Aeronautics', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'HINDPETRO.NS', 'name': 'Hindustan Petroleum Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'HINDZINC.NS', 'name': 'Hindustan Zinc', 'sector': 'metals', 'marketCap': 'mid'},
        {'symbol': 'HUDCO.NS', 'name': 'Housing & Urban Development Corporation', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'HYUNDAI.NS', 'name': 'Hyundai Motor India', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'ICICIGI.NS', 'name': 'ICICI Lombard General Insurance Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'ICICIPRULI.NS', 'name': 'ICICI Prudential Life Insurance Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'IDFCFIRSTB.NS', 'name': 'IDFC First Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'IRB.NS', 'name': 'IRB Infrastructure Developers', 'sector': 'construction', 'marketCap': 'mid'},
        {'symbol': 'ITC.NS', 'name': 'ITC', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'INDIANB.NS', 'name': 'Indian Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'INDHOTEL.NS', 'name': 'Indian Hotels Co.', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'IOC.NS', 'name': 'Indian Oil Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'IRCTC.NS', 'name': 'Indian Railway Catering And Tourism Corporation', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'IRFC.NS', 'name': 'Indian Railway Finance Corporation', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'IREDA.NS', 'name': 'Indian Renewable Energy Development Agency', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'IGL.NS', 'name': 'Indraprastha Gas', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'INDUSTOWER.NS', 'name': 'Indus Towers', 'sector': 'telecom', 'marketCap': 'mid'},
        {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'NAUKRI.NS', 'name': 'Info Edge (India)', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'INFY.NS', 'name': 'Infosys', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'INDIGO.NS', 'name': 'InterGlobe Aviation', 'sector': 'infrastructure', 'marketCap': 'mid'},
        {'symbol': 'JSWENERGY.NS', 'name': 'JSW Energy', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'JSWINFRA.NS', 'name': 'JSW Infrastructure', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'JINDALSTEL.NS', 'name': 'Jindal Steel & Power', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'JIOFIN.NS', 'name': 'Jio Financial Services', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'JUBLFOOD.NS', 'name': 'Jubilant FoodWorks', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'KPITTECH.NS', 'name': 'KPIT Technologies', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'KANSAINER.NS', 'name': 'Kansai Nerolac Paints', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'KEI.NS', 'name': 'KEI Industries', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'LTIM.NS', 'name': 'LTIMindtree', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'LTTS.NS', 'name': 'L&T Technology Services', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'sector': 'construction', 'marketCap': 'small'},
        {'symbol': 'LICHSGFIN.NS', 'name': 'LIC Housing Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'LICI.NS', 'name': 'Life Insurance Corporation of India', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'LODHA.NS', 'name': 'Lodha Developers', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'LUPIN.NS', 'name': 'Lupin', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'M&MFIN.NS', 'name': 'Mahindra & Mahindra Financial Services', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'MFSL.NS', 'name': 'Max Financial Services', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'MGL.NS', 'name': 'Mahanagar Gas', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'MAHINDCIE.NS', 'name': 'Mahindra CIE Automotive', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'MANAPPURAM.NS', 'name': 'Manappuram Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'MARICO.NS', 'name': 'Marico', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'METROPOLIS.NS', 'name': 'Metropolis Healthcare', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'MRF.NS', 'name': 'MRF', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'MOTHERSON.NS', 'name': 'Samvardhana Motherson International', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'MPHASIS.NS', 'name': 'Mphasis', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'MRPL.NS', 'name': 'Mangalore Refinery and Petrochemicals', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'MUTHOOTFIN.NS', 'name': 'Muthoot Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'NATIONALUM.NS', 'name': 'National Aluminium Company', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'NIACL.NS', 'name': 'The New India Assurance Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'NMDC.NS', 'name': 'NMDC', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'NTPC.NS', 'name': 'NTPC', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'OBEROIRLTY.NS', 'name': 'Oberoi Realty', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'ONGC.NS', 'name': 'Oil & Natural Gas Corporation', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'OIL.NS', 'name': 'Oil India', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'PAYTM.NS', 'name': 'One 97 Communications', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'PAGEIND.NS', 'name': 'Page Industries', 'sector': 'textiles', 'marketCap': 'small'},
        {'symbol': 'PERSISTENT.NS', 'name': 'Persistent Systems', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'PETRONET.NS', 'name': 'Petronet LNG', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'PFIZER.NS', 'name': 'Pfizer', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'PIDILITIND.NS', 'name': 'Pidilite Industries', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'PIIND.NS', 'name': 'PI Industries', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'PFC.NS', 'name': 'Power Finance Corporation', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corporation of India', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'PRESTIGE.NS', 'name': 'Prestige Estates Projects', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'PVRINOX.NS', 'name': 'PVR INOX', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'PNB.NS', 'name': 'Punjab National Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'POLYCAB.NS', 'name': 'Polycab India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'RBLBANK.NS', 'name': 'RBL Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'RECLTD.NS', 'name': 'REC', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'SAIL.NS', 'name': 'Steel Authority of India', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'SBICARD.NS', 'name': 'SBI Cards and Payment Services', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'SBILIFE.NS', 'name': 'SBI Life Insurance Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'SJVN.NS', 'name': 'SJVN', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'SKFINDIA.NS', 'name': 'SKF India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'SOBHA.NS', 'name': 'Sobha', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'SOLARINDS.NS', 'name': 'Solar Industries India', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'SONACOMS.NS', 'name': 'Sona BLW Precision Forgings', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'SHREECEM.NS', 'name': 'Shree Cement', 'sector': 'cement', 'marketCap': 'small'},
        {'symbol': 'SHRIRAMFIN.NS', 'name': 'Shriram Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'SIEMENS.NS', 'name': 'Siemens', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical Industries', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'SUNTV.NS', 'name': 'Sun TV Network', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'SWIGGY.NS', 'name': 'Swiggy', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'SYMPHONY.NS', 'name': 'Symphony', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'SYNGENE.NS', 'name': 'Syngene International', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'TVSMOTOR.NS', 'name': 'TVS Motor Company', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'TATACOMM.NS', 'name': 'Tata Communications', 'sector': 'telecom', 'marketCap': 'small'},
        {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer Products', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'TATAELXSI.NS', 'name': 'Tata Elxsi', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'TATAPOWER.NS', 'name': 'Tata Power Co.', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'THERMAX.NS', 'name': 'Thermax', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'TIINDIA.NS', 'name': 'Tube Investments of India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'TITAN.NS', 'name': 'Titan Company', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'TORNTPHARM.NS', 'name': 'Torrent Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'TRENT.NS', 'name': 'Trent', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'TTML.NS', 'name': 'Tata Teleservices (Maharashtra)', 'sector': 'telecom', 'marketCap': 'small'},
        {'symbol': 'UBL.NS', 'name': 'United Breweries', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement', 'sector': 'cement', 'marketCap': 'small'},
        {'symbol': 'UNIONBANK.NS', 'name': 'Union Bank of India', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'UNITDSPR.NS', 'name': 'United Spirits', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'UPL.NS', 'name': 'UPL', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'VBL.NS', 'name': 'Varun Beverages', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'VEDL.NS', 'name': 'Vedanta', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'VINATIORGA.NS', 'name': 'Vinati Organics', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'VOLTAS.NS', 'name': 'Voltas', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'WHIRLPOOL.NS', 'name': 'Whirlpool of India', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'YESBANK.NS', 'name': 'Yes Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ZYDUSLIFE.NS', 'name': 'Zydus Lifesciences', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'ZOMATO.NS', 'name': 'Zomato', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'ZEEL.NS', 'name': 'Zee Entertainment Enterprises', 'sector': 'consumer', 'marketCap': 'small'}
    ]
    
def get_nifty_500_stocks():
    """Nifty 500 stocks - comprehensive list of top 500+ Indian companies"""
    return [
        # Large Cap (1-50)
        {'symbol': '360ONE.NS', 'name': '360 ONE WAM', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': '3MINDIA.NS', 'name': '3M India', 'sector': 'diversified', 'marketCap': 'large'},
        {'symbol': 'ABB.NS', 'name': 'ABB India', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ACC.NS', 'name': 'ACC', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'ACMESOLAR.NS', 'name': 'ACME Solar Holdings', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'AIAENG.NS', 'name': 'AIA Engineering', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'APLAPOLLO.NS', 'name': 'APL Apollo Tubes', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'AUBANK.NS', 'name': 'AU Small Finance Bank', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'AWL.NS', 'name': 'AWL Agri Business', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'AADHARHFC.NS', 'name': 'Aadhar Housing Finance', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'AARTIIND.NS', 'name': 'Aarti Industries', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'AAVAS.NS', 'name': 'Aavas Financiers', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ABCAPITAL.NS', 'name': 'Aditya Birla Capital', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ABFRL.NS', 'name': 'Aditya Birla Fashion and Retail', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'ADANIENSOL.NS', 'name': 'Adani Energy Solutions', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIENT.NS', 'name': 'Adani Enterprises', 'sector': 'metals', 'marketCap': 'large'},
        {'symbol': 'ADANIGREEN.NS', 'name': 'Adani Green Energy', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports and Special Economic Zone', 'sector': 'infrastructure', 'marketCap': 'large'},
        {'symbol': 'ADANIPOWER.NS', 'name': 'Adani Power', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ATGL.NS', 'name': 'Adani Total Gas', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'ADANIWILMAR.NS', 'name': 'Adani Wilmar', 'sector': 'fmcg', 'marketCap': 'large'},
        {'symbol': 'AEGISLOG.NS', 'name': 'Aegis Logistics', 'sector': 'energy', 'marketCap': 'large'},
        {'symbol': 'AETHER.NS', 'name': 'Aether Industries', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'AFFLE.NS', 'name': 'Affle (India)', 'sector': 'it', 'marketCap': 'large'},
        {'symbol': 'AJANTPHARM.NS', 'name': 'Ajanta Pharma', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'AKZOINDIA.NS', 'name': 'Akzo Nobel India', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'ALKEM.NS', 'name': 'Alkem Laboratories', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'ALKYLAMINE.NS', 'name': 'Alkyl Amines Chemicals', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'ALLCARGO.NS', 'name': 'Allcargo Logistics', 'sector': 'infrastructure', 'marketCap': 'large'},
        {'symbol': 'ALOKINDS.NS', 'name': 'Alok Industries', 'sector': 'textiles', 'marketCap': 'large'},
        {'symbol': 'AMBER.NS', 'name': 'Amber Enterprises India', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'AMBUJACEM.NS', 'name': 'Ambuja Cements', 'sector': 'cement', 'marketCap': 'large'},
        {'symbol': 'ANANTRAJ.NS', 'name': 'Anant Raj', 'sector': 'realty', 'marketCap': 'large'},
        {'symbol': 'ANGELONE.NS', 'name': 'Angel One', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ANILAINFRA.NS', 'name': 'Anil Starch Products', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'APARINDS.NS', 'name': 'Apar Industries', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals Enterprise', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'APOLLOTYRE.NS', 'name': 'Apollo Tyres', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'APTUS.NS', 'name': 'Aptus Value Housing Finance India', 'sector': 'banking', 'marketCap': 'large'},
        {'symbol': 'ASAHIINDIA.NS', 'name': 'Asahi India Glass', 'sector': 'auto', 'marketCap': 'large'},
        {'symbol': 'ASHOKLEY.NS', 'name': 'Ashok Leyland', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'ASTERDM.NS', 'name': 'Aster DM Healthcare', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'ASTRAL.NS', 'name': 'Astral', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ASTRAZEN.NS', 'name': 'AstraZeneca Pharma India', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'ATLANTAA.NS', 'name': 'Atlantaa', 'sector': 'capital_goods', 'marketCap': 'large'},
        {'symbol': 'ATUL.NS', 'name': 'Atul', 'sector': 'chemicals', 'marketCap': 'large'},
        {'symbol': 'AUROPHARMA.NS', 'name': 'Aurobindo Pharma', 'sector': 'healthcare', 'marketCap': 'large'},
        {'symbol': 'DMART.NS', 'name': 'Avenue Supermarts', 'sector': 'consumer', 'marketCap': 'large'},
        {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank', 'sector': 'banking', 'marketCap': 'large'},
        
        # Mid Cap (51-100)
        {'symbol': 'BSE.NS', 'name': 'BSE', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BAJAJHLDNG.NS', 'name': 'Bajaj Holdings & Investment', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BAJAJHFL.NS', 'name': 'Bajaj Housing Finance', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BALKRISIND.NS', 'name': 'Balkrishna Industries', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'BALRAMCHIN.NS', 'name': 'Balrampur Chini Mills', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'BANDHANBNK.NS', 'name': 'Bandhan Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BANKBARODA.NS', 'name': 'Bank of Baroda', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BANKINDIA.NS', 'name': 'Bank of India', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'MAHABANK.NS', 'name': 'Bank of Maharashtra', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'BASF.NS', 'name': 'BASF India', 'sector': 'chemicals', 'marketCap': 'mid'},
        {'symbol': 'BATAINDIA.NS', 'name': 'Bata India', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'BAYERCROP.NS', 'name': 'Bayer CropScience', 'sector': 'chemicals', 'marketCap': 'mid'},
        {'symbol': 'BDL.NS', 'name': 'Bharat Dynamics', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'BEL.NS', 'name': 'Bharat Electronics', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'BHARATFORG.NS', 'name': 'Bharat Forge', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'BHEL.NS', 'name': 'Bharat Heavy Electricals', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'BPCL.NS', 'name': 'Bharat Petroleum Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel', 'sector': 'telecom', 'marketCap': 'mid'},
        {'symbol': 'BHARTIHEXA.NS', 'name': 'Bharti Hexacom', 'sector': 'telecom', 'marketCap': 'mid'},
        {'symbol': 'BIKAJI.NS', 'name': 'Bikaji Foods International', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'BIOCON.NS', 'name': 'Biocon', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'BIRLACORPN.NS', 'name': 'Birla Corporation', 'sector': 'cement', 'marketCap': 'mid'},
        {'symbol': 'BSOFT.NS', 'name': 'Birlasoft', 'sector': 'it', 'marketCap': 'mid'},
        {'symbol': 'BLISSGVS.NS', 'name': 'Bliss GVS Pharma', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'BLUEDART.NS', 'name': 'Blue Dart Express', 'sector': 'infrastructure', 'marketCap': 'mid'},
        {'symbol': 'BLUESTARCO.NS', 'name': 'Blue Star', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'BOSCHLTD.NS', 'name': 'Bosch', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'BRIGADE.NS', 'name': 'Brigade Enterprises', 'sector': 'realty', 'marketCap': 'mid'},
        {'symbol': 'BRITANNIA.NS', 'name': 'Britannia Industries', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'CCL.NS', 'name': 'CCL Products (India)', 'sector': 'fmcg', 'marketCap': 'mid'},
        {'symbol': 'CESC.NS', 'name': 'CESC', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'CGPOWER.NS', 'name': 'CG Power and Industrial Solutions', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'CAMS.NS', 'name': 'Computer Age Management Services', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'CANBK.NS', 'name': 'Canara Bank', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'CANFINHOME.NS', 'name': 'Can Fin Homes', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'CAPLIPOINT.NS', 'name': 'Caplin Point Laboratories', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'CARBORUNIV.NS', 'name': 'Carborundum Universal', 'sector': 'capital_goods', 'marketCap': 'mid'},
        {'symbol': 'CASTROLIND.NS', 'name': 'Castrol India', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'CEATLTD.NS', 'name': 'CEAT', 'sector': 'auto', 'marketCap': 'mid'},
        {'symbol': 'CENTURYTEX.NS', 'name': 'Century Textiles & Industries', 'sector': 'textiles', 'marketCap': 'mid'},
        {'symbol': 'CERA.NS', 'name': 'Cera Sanitaryware', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'CHALET.NS', 'name': 'Chalet Hotels', 'sector': 'consumer', 'marketCap': 'mid'},
        {'symbol': 'CHAMBLFERT.NS', 'name': 'Chambal Fertilizers & Chemicals', 'sector': 'chemicals', 'marketCap': 'mid'},
        {'symbol': 'CHENNPETRO.NS', 'name': 'Chennai Petroleum Corporation', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'CHOLAFIN.NS', 'name': 'Cholamandalam Investment and Finance Company', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'CHOLAHLDNG.NS', 'name': 'Cholamandalam Financial Holdings', 'sector': 'banking', 'marketCap': 'mid'},
        {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'sector': 'healthcare', 'marketCap': 'mid'},
        {'symbol': 'COALINDIA.NS', 'name': 'Coal India', 'sector': 'energy', 'marketCap': 'mid'},
        {'symbol': 'COCHINSHIP.NS', 'name': 'Cochin Shipyard', 'sector': 'capital_goods', 'marketCap': 'mid'},
        
        # Small Cap (101-250)
        {'symbol': 'COFORGE.NS', 'name': 'Coforge', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'COLPAL.NS', 'name': 'Colgate Palmolive (India)', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'CONCOR.NS', 'name': 'Container Corporation of India', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'COROMANDEL.NS', 'name': 'Coromandel International', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'CREDITACC.NS', 'name': 'Credit Access Grameen', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'CROMPTON.NS', 'name': 'Crompton Greaves Consumer Electricals', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'CUMMINSIND.NS', 'name': 'Cummins India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'CYIENT.NS', 'name': 'Cyient', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'DLF.NS', 'name': 'DLF', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'DABUR.NS', 'name': 'Dabur India', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'DALMIASUG.NS', 'name': 'Dalmia Bharat Sugar and Industries', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'DEEPAKNTR.NS', 'name': 'Deepak Nitrite', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'DELTACORP.NS', 'name': 'Delta Corp', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'DEVYANI.NS', 'name': 'Devyani International', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'DIVISLAB.NS', 'name': 'Divi\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'DIXON.NS', 'name': 'Dixon Technologies (India)', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddy\'s Laboratories', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'EIDPARRY.NS', 'name': 'EID Parry (India)', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'EIHOTEL.NS', 'name': 'EIH', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'ELGIEQUIP.NS', 'name': 'Elgi Equipments', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'EMAMILTD.NS', 'name': 'Emami', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'ENDURANCE.NS', 'name': 'Endurance Technologies', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'ENGINERSIN.NS', 'name': 'Engineers India', 'sector': 'construction', 'marketCap': 'small'},
        {'symbol': 'EQUITAS.NS', 'name': 'Equitas Small Finance Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ESCORTS.NS', 'name': 'Escorts Kubota', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'ESABINDIA.NS', 'name': 'Esab India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'ETERNAL.NS', 'name': 'Eternal', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'EVEREADY.NS', 'name': 'Eveready Industries India', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'EXIDEIND.NS', 'name': 'Exide Industries', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'NYKAA.NS', 'name': 'FSN E-Commerce Ventures', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'FINEORG.NS', 'name': 'Fine Organic Industries', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'FINPIPE.NS', 'name': 'Finolex Cables', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'FEDERALBNK.NS', 'name': 'Federal Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'FORTIS.NS', 'name': 'Fortis Healthcare', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'FRETAIL.NS', 'name': 'Future Retail', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'GAIL.NS', 'name': 'GAIL (India)', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'GARFIBRES.NS', 'name': 'Garware Technical Fibres', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'GMRAIRPORT.NS', 'name': 'GMR Airports', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'GNFC.NS', 'name': 'Gujarat Narmada Valley Fertilizers & Chemicals', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'GLENMARK.NS', 'name': 'Glenmark Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'GLAXO.NS', 'name': 'GlaxoSmithKline Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'GMDCLTD.NS', 'name': 'Gujarat Mineral Development Corporation', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'GMRINFRA.NS', 'name': 'GMR Infrastructure', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'GODFRYPHLP.NS', 'name': 'Godfrey Phillips India', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'GODREJCP.NS', 'name': 'Godrej Consumer Products', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'GODREJIND.NS', 'name': 'Godrej Industries', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'GODREJPROP.NS', 'name': 'Godrej Properties', 'sector': 'realty', 'marketCap': 'small'},
        {'symbol': 'GRANULES.NS', 'name': 'Granules India', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'GRAPHITE.NS', 'name': 'Graphite India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries', 'sector': 'cement', 'marketCap': 'small'},
        {'symbol': 'GRINFRA.NS', 'name': 'G R Infraprojects', 'sector': 'construction', 'marketCap': 'small'},
        {'symbol': 'GESHIP.NS', 'name': 'Great Eastern Shipping Company', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'GRSE.NS', 'name': 'Garden Reach Shipbuilders & Engineers', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'GSFC.NS', 'name': 'Gujarat State Fertilizers & Chemicals', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'GSPL.NS', 'name': 'Gujarat State Petronet', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'GUJGASLTD.NS', 'name': 'Gujarat Gas', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'GULFOILLUB.NS', 'name': 'Gulf Oil Lubricants India', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'HCG.NS', 'name': 'HealthCare Global Enterprises', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'HDFCAMC.NS', 'name': 'HDFC Asset Management Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life Insurance Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'HFCL.NS', 'name': 'HFCL', 'sector': 'telecom', 'marketCap': 'small'},
        {'symbol': 'HLEGLAS.NS', 'name': 'HLE Glascoat', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'HMVL.NS', 'name': 'Hindustan Media Ventures', 'sector': 'media', 'marketCap': 'small'},
        {'symbol': 'HONAUT.NS', 'name': 'Honeywell Automation India', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'HUDCO.NS', 'name': 'Housing & Urban Development Corporation', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'HAVELLS.NS', 'name': 'Havells India', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'HEIDELBERG.NS', 'name': 'HeidelbergCement India', 'sector': 'cement', 'marketCap': 'small'},
        {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'HEXAWARE.NS', 'name': 'Hexaware Technologies', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'HICAL.NS', 'name': 'Hical Chemicals', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'HAL.NS', 'name': 'Hindustan Aeronautics', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'HINDCOPPER.NS', 'name': 'Hindustan Copper', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'HINDPETRO.NS', 'name': 'Hindustan Petroleum Corporation', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever', 'sector': 'fmcg', 'marketCap': 'small'},
        {'symbol': 'HINDZINC.NS', 'name': 'Hindustan Zinc', 'sector': 'metals', 'marketCap': 'small'},
        {'symbol': 'HINDUSTANBIOSCI.NS', 'name': 'Hindustan BioSciences', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'HIMATSEIDE.NS', 'name': 'Himatsingka Seide', 'sector': 'textiles', 'marketCap': 'small'},
        {'symbol': 'HPL.NS', 'name': 'HPL Electric & Power', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'HSIL.NS', 'name': 'HSIL', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'HYUNDAI.NS', 'name': 'Hyundai Motor India', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'IBULHSGFIN.NS', 'name': 'Indiabulls Housing Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ICICIGI.NS', 'name': 'ICICI Lombard General Insurance Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ICICIPRULI.NS', 'name': 'ICICI Prudential Life Insurance Company', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'IDEA.NS', 'name': 'Vodafone Idea', 'sector': 'telecom', 'marketCap': 'small'},
        {'symbol': 'IDFCFIRSTB.NS', 'name': 'IDFC First Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'IEX.NS', 'name': 'Indian Energy Exchange', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'IFBIND.NS', 'name': 'IFB Industries', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'IGARASHI.NS', 'name': 'Igarashi Motors India', 'sector': 'auto', 'marketCap': 'small'},
        {'symbol': 'IIFL.NS', 'name': 'India Infoline Finance', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'INDIACEM.NS', 'name': 'The India Cements', 'sector': 'cement', 'marketCap': 'small'},
        {'symbol': 'INDIAMART.NS', 'name': 'IndiaMART InterMESH', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'INDIANB.NS', 'name': 'Indian Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'INDHOTEL.NS', 'name': 'Indian Hotels Co.', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'IOC.NS', 'name': 'Indian Oil Corporation', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'IRCTC.NS', 'name': 'Indian Railway Catering And Tourism Corporation', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'IRFC.NS', 'name': 'Indian Railway Finance Corporation', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'IREDA.NS', 'name': 'Indian Renewable Energy Development Agency', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'INDIGO.NS', 'name': 'InterGlobe Aviation', 'sector': 'infrastructure', 'marketCap': 'small'},
        {'symbol': 'IGL.NS', 'name': 'Indraprastha Gas', 'sector': 'energy', 'marketCap': 'small'},
        {'symbol': 'INDUSTOWER.NS', 'name': 'Indus Towers', 'sector': 'telecom', 'marketCap': 'small'},
        {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'NAUKRI.NS', 'name': 'Info Edge (India)', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'INFY.NS', 'name': 'Infosys', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'INGERRAND.NS', 'name': 'Ingersoll Rand (India)', 'sector': 'capital_goods', 'marketCap': 'small'},
        {'symbol': 'INOXLEISUR.NS', 'name': 'INOX Leisure', 'sector': 'consumer', 'marketCap': 'small'},
        {'symbol': 'INSECTICID.NS', 'name': 'Insecticides (India)', 'sector': 'chemicals', 'marketCap': 'small'},
        {'symbol': 'INTELLECT.NS', 'name': 'Intellect Design Arena', 'sector': 'it', 'marketCap': 'small'},
        {'symbol': 'IPCALAB.NS', 'name': 'IPCA Laboratories', 'sector': 'healthcare', 'marketCap': 'small'},
        {'symbol': 'IRB.NS', 'name': 'IRB Infrastructure Developers', 'sector': 'construction', 'marketCap': 'small'},
        {'symbol': 'ISEC.NS', 'name': 'IIFL Securities', 'sector': 'banking', 'marketCap': 'small'},
        {'symbol': 'ITC.NS', 'name': 'ITC', 'sector': 'fmcg', 'marketCap': 'small'},
        
        # Micro Cap (251-501)
        {'symbol': 'ITDCEM.NS', 'name': 'ITD Cementation India', 'sector': 'construction', 'marketCap': 'micro'},
        {'symbol': 'JSWENERGY.NS', 'name': 'JSW Energy', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'JSWINFRA.NS', 'name': 'JSW Infrastructure', 'sector': 'infrastructure', 'marketCap': 'micro'},
        {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'JBCHEPHARM.NS', 'name': 'JB Chemicals & Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'JKCEMENT.NS', 'name': 'JK Cement', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'JKLAKSHMI.NS', 'name': 'JK Lakshmi Cement', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'JKPAPER.NS', 'name': 'JK Paper', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'JKTYRE.NS', 'name': 'JK Tyre & Industries', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'JMFINANCIL.NS', 'name': 'JM Financial', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'JSLHISAR.NS', 'name': 'Jindal Stainless (Hisar)', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'JINDALSTEL.NS', 'name': 'Jindal Steel & Power', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'JIOFIN.NS', 'name': 'Jio Financial Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'JYOTHYLAB.NS', 'name': 'Jyothy Labs', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'JUBLFOOD.NS', 'name': 'Jubilant FoodWorks', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'JUBLINGREA.NS', 'name': 'Jubilant Ingrevia', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'JUSTDIAL.NS', 'name': 'Just Dial', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'JYOTHYLAB.NS', 'name': 'Jyothy Labs', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'KAJARIACER.NS', 'name': 'Kajaria Ceramics', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'KALPATPOWR.NS', 'name': 'Kalpataru Power Transmission', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KANSAINER.NS', 'name': 'Kansai Nerolac Paints', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'KAPURPESTH.NS', 'name': 'Kapur Pesticides', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'KARURVYSYA.NS', 'name': 'Karur Vysya Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'KECL.NS', 'name': 'Kirloskar Electric Company', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KEI.NS', 'name': 'KEI Industries', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KENNAMET.NS', 'name': 'Kennametal India', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KFINTECH.NS', 'name': 'KFin Technologies', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'KHADIM.NS', 'name': 'Khadim India', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'KIOCL.NS', 'name': 'KIOCL', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'KIRLOSENG.NS', 'name': 'Kirloskar Brothers', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KIRLFER.NS', 'name': 'Kirloskar Ferrous Industries', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'KIRLOSBROS.NS', 'name': 'Kirloskar Brothers', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KIRIINDUS.NS', 'name': 'Kiri Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'KPITTECH.NS', 'name': 'KPIT Technologies', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'KRBL.NS', 'name': 'KRBL', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'KSB.NS', 'name': 'KSB', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'KTKBANK.NS', 'name': 'Karnataka Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'L&TFH.NS', 'name': 'L&T Finance Holdings', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'LTIM.NS', 'name': 'LTIMindtree', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'LTTS.NS', 'name': 'L&T Technology Services', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'LEMONTREE.NS', 'name': 'Lemon Tree Hotels', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'sector': 'construction', 'marketCap': 'micro'},
        {'symbol': 'LAURUSLABS.NS', 'name': 'Laurus Labs', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'LICHSGFIN.NS', 'name': 'LIC Housing Finance', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'LICI.NS', 'name': 'Life Insurance Corporation of India', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'LINDEINDIA.NS', 'name': 'Linde India', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'LODHA.NS', 'name': 'Lodha Developers', 'sector': 'realty', 'marketCap': 'micro'},
        {'symbol': 'LUPIN.NS', 'name': 'Lupin', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'LXCHEM.NS', 'name': 'Laxmi Organic Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'LYKALABS.NS', 'name': 'Lyka Labs', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'M&MFIN.NS', 'name': 'Mahindra & Mahindra Financial Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'MFSL.NS', 'name': 'Max Financial Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'MGL.NS', 'name': 'Mahanagar Gas', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'MAHINDCIE.NS', 'name': 'Mahindra CIE Automotive', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MAJESCO.NS', 'name': 'Majesco', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'MANAPPURAM.NS', 'name': 'Manappuram Finance', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'MARICO.NS', 'name': 'Marico', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MASTEK.NS', 'name': 'Mastek', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'MAXHEALTH.NS', 'name': 'Max Healthcare Institute', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'MAZDOCK.NS', 'name': 'Mazagon Dock Shipbuilders', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'MCDOWELL-N.NS', 'name': 'United Spirits', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'MCX.NS', 'name': 'Multi Commodity Exchange of India', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'MEDPLUS.NS', 'name': 'MedPlus Health Services', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'METROPOLIS.NS', 'name': 'Metropolis Healthcare', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'MHRIL.NS', 'name': 'Mahindra Holidays & Resorts India', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'MIDHANI.NS', 'name': 'Mishra Dhatu Nigam', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'MINDACORP.NS', 'name': 'Minda Corporation', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MINDTREE.NS', 'name': 'Mindtree', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'MOLDTKPAC.NS', 'name': 'Mold-Tek Packaging', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'MOIL.NS', 'name': 'MOIL', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'MRF.NS', 'name': 'MRF', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MOTHERSON.NS', 'name': 'Samvardhana Motherson International', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MOTILALOFS.NS', 'name': 'Motilal Oswal Financial Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'MPHASIS.NS', 'name': 'Mphasis', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'MRPL.NS', 'name': 'Mangalore Refinery and Petrochemicals', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'MSUMI.NS', 'name': 'Motherson Sumi Wiring India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'MTARTECH.NS', 'name': 'MTAR Technologies', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'MUTHOOTFIN.NS', 'name': 'Muthoot Finance', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'NALCO.NS', 'name': 'National Aluminium Company', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'NATIONALUM.NS', 'name': 'National Aluminium Company', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'NAVINFLUOR.NS', 'name': 'Navin Fluorine International', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'NESCO.NS', 'name': 'Nesco', 'sector': 'infrastructure', 'marketCap': 'micro'},
        {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'NETWORK18.NS', 'name': 'Network18 Media & Investments', 'sector': 'media', 'marketCap': 'micro'},
        {'symbol': 'NEWGEN.NS', 'name': 'Newgen Software Technologies', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'NIACL.NS', 'name': 'The New India Assurance Company', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'NIITLTD.NS', 'name': 'NIIT', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'NILKAMAL.NS', 'name': 'Nilkamal', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'NLCINDIA.NS', 'name': 'NLC India', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'NMDC.NS', 'name': 'NMDC', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'NOCIL.NS', 'name': 'NOCIL', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'NSLNISP.NS', 'name': 'NSIL', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'NTPC.NS', 'name': 'NTPC', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'NUCLEUS.NS', 'name': 'Nucleus Software Exports', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'OBEROIRLTY.NS', 'name': 'Oberoi Realty', 'sector': 'realty', 'marketCap': 'micro'},
        {'symbol': 'OFSS.NS', 'name': 'Oracle Financial Services Software', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'OIL.NS', 'name': 'Oil India', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'ONGC.NS', 'name': 'Oil & Natural Gas Corporation', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'ORIENTELEC.NS', 'name': 'Orient Electric', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'PAYTM.NS', 'name': 'One 97 Communications', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'PNBGILTS.NS', 'name': 'PNB Gilts', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'PNCINFRA.NS', 'name': 'PNC Infratech', 'sector': 'construction', 'marketCap': 'micro'},
        {'symbol': 'PAGEIND.NS', 'name': 'Page Industries', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'PARAGMILK.NS', 'name': 'Parag Milk Foods', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'PERSISTENT.NS', 'name': 'Persistent Systems', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'PETRONET.NS', 'name': 'Petronet LNG', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'PFIZER.NS', 'name': 'Pfizer', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'PHOENIXLTD.NS', 'name': 'The Phoenix Mills', 'sector': 'realty', 'marketCap': 'micro'},
        {'symbol': 'PIDILITIND.NS', 'name': 'Pidilite Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'PIIND.NS', 'name': 'PI Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'PIRAMALENT.NS', 'name': 'Piramal Enterprises', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'POLICYBZR.NS', 'name': 'PB Fintech', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'POLYMED.NS', 'name': 'Poly Medicure', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'POLYCAB.NS', 'name': 'Polycab India', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'POLYPLEX.NS', 'name': 'Polyplex Corporation', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'POONAWALLA.NS', 'name': 'Poonawalla Fincorp', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'PFC.NS', 'name': 'Power Finance Corporation', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corporation of India', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'PRAJIND.NS', 'name': 'Praj Industries', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'PRESTIGE.NS', 'name': 'Prestige Estates Projects', 'sector': 'realty', 'marketCap': 'micro'},
        {'symbol': 'PRINCEPIPE.NS', 'name': 'Prince Pipes and Fittings', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'PRSMJOHNSN.NS', 'name': 'Prism Johnson', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'PVR.NS', 'name': 'PVR', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'PVRINOX.NS', 'name': 'PVR INOX', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'PNB.NS', 'name': 'Punjab National Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'QUESS.NS', 'name': 'Quess Corp', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'RADICO.NS', 'name': 'Radico Khaitan', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'RAIN.NS', 'name': 'Rain Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'RAJESHEXPO.NS', 'name': 'Rajesh Exports', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'RALLIS.NS', 'name': 'Rallis India', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'RAMCOCEM.NS', 'name': 'The Ramco Cements', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'RATEGAIN.NS', 'name': 'RateGain Travel Technologies', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'RATNAMANI.NS', 'name': 'Ratnamani Metals & Tubes', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'RAYMOND.NS', 'name': 'Raymond', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'RBL.NS', 'name': 'Rane Brake Lining', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'RBLBANK.NS', 'name': 'RBL Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'RECLTD.NS', 'name': 'REC', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'REDINGTON.NS', 'name': 'Redington', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'RELAXO.NS', 'name': 'Relaxo Footwears', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'RENUKA.NS', 'name': 'Shree Renuka Sugars', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'REXPIPES.NS', 'name': 'RGP Pipes', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'RITES.NS', 'name': 'RITES', 'sector': 'construction', 'marketCap': 'micro'},
        {'symbol': 'ROUTE.NS', 'name': 'Route Mobile', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'RSYSTEMS.NS', 'name': 'R Systems International', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'SAFARI.NS', 'name': 'Safari Industries (India)', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SAIL.NS', 'name': 'Steel Authority of India', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'SANOFI.NS', 'name': 'Sanofi India', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'SAREGAMA.NS', 'name': 'Saregama India', 'sector': 'media', 'marketCap': 'micro'},
        {'symbol': 'SBICARD.NS', 'name': 'SBI Cards and Payment Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'SBILIFE.NS', 'name': 'SBI Life Insurance Company', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'SCHAEFFLER.NS', 'name': 'Schaeffler India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'SEQUENT.NS', 'name': 'Sequent Scientific', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'SFL.NS', 'name': 'Sheela Foam', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SHOPERSTOP.NS', 'name': 'Shoppers Stop', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SHREECEM.NS', 'name': 'Shree Cement', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'SHREYAS.NS', 'name': 'Shreyas Shipping & Logistics', 'sector': 'infrastructure', 'marketCap': 'micro'},
        {'symbol': 'SHRIRAMFIN.NS', 'name': 'Shriram Finance', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'SIEMENS.NS', 'name': 'Siemens', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'SIS.NS', 'name': 'SIS', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SJVN.NS', 'name': 'SJVN', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'SKFINDIA.NS', 'name': 'SKF India', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'SOBHA.NS', 'name': 'Sobha', 'sector': 'realty', 'marketCap': 'micro'},
        {'symbol': 'SOLARINDS.NS', 'name': 'Solar Industries India', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'SONACOMS.NS', 'name': 'Sona BLW Precision Forgings', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'STAR.NS', 'name': 'Strides Pharma Science', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'STARHEALTH.NS', 'name': 'Star Health and Allied Insurance Company', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'SUDARSCHEM.NS', 'name': 'Sudarshan Chemical Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'SUMICHEM.NS', 'name': 'Sumitomo Chemical India', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical Industries', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'SUNTV.NS', 'name': 'Sun TV Network', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SUPRAJIT.NS', 'name': 'Suprajit Engineering', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'SUPREMEIND.NS', 'name': 'Supreme Industries', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'SWANENERGY.NS', 'name': 'Swan Energy', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'SWIGGY.NS', 'name': 'Swiggy', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SYMPHONY.NS', 'name': 'Symphony', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'SYNGENE.NS', 'name': 'Syngene International', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'TATACHEM.NS', 'name': 'Tata Chemicals', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'TATACOMM.NS', 'name': 'Tata Communications', 'sector': 'telecom', 'marketCap': 'micro'},
        {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer Products', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'TATAELXSI.NS', 'name': 'Tata Elxsi', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'TATAINVEST.NS', 'name': 'Tata Investment Corporation', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'TATAPOWER.NS', 'name': 'Tata Power Co.', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'TVSMOTOR.NS', 'name': 'TVS Motor Company', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'TEAMLEASE.NS', 'name': 'TeamLease Services', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'TEJASNET.NS', 'name': 'Tejas Networks', 'sector': 'telecom', 'marketCap': 'micro'},
        {'symbol': 'THERMAX.NS', 'name': 'Thermax', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'THYROCARE.NS', 'name': 'Thyrocare Technologies', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'TIINDIA.NS', 'name': 'Tube Investments of India', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'TIMKEN.NS', 'name': 'Timken India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'TITAN.NS', 'name': 'Titan Company', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'TORNTPHARM.NS', 'name': 'Torrent Pharmaceuticals', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'TORNTPOWER.NS', 'name': 'Torrent Power', 'sector': 'energy', 'marketCap': 'micro'},
        {'symbol': 'TRENT.NS', 'name': 'Trent', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'TRIDENT.NS', 'name': 'Trident', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'TRITURBINE.NS', 'name': 'Triveni Turbine', 'sector': 'capital_goods', 'marketCap': 'micro'},
        {'symbol': 'TTML.NS', 'name': 'Tata Teleservices (Maharashtra)', 'sector': 'telecom', 'marketCap': 'micro'},
        {'symbol': 'UJJIVAN.NS', 'name': 'Ujjivan Financial Services', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'UBL.NS', 'name': 'United Breweries', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement', 'sector': 'cement', 'marketCap': 'micro'},
        {'symbol': 'UNIONBANK.NS', 'name': 'Union Bank of India', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'UNITDSPR.NS', 'name': 'United Spirits', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'UPL.NS', 'name': 'UPL', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'UTIAMC.NS', 'name': 'UTI Asset Management Company', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'VBL.NS', 'name': 'Varun Beverages', 'sector': 'fmcg', 'marketCap': 'micro'},
        {'symbol': 'VEDL.NS', 'name': 'Vedanta', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'VIJAYA.NS', 'name': 'Vijaya Diagnostic Centre', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'VINATIORGA.NS', 'name': 'Vinati Organics', 'sector': 'chemicals', 'marketCap': 'micro'},
        {'symbol': 'VIPIND.NS', 'name': 'VIP Industries', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'VMART.NS', 'name': 'V-Mart Retail', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'VOLTAS.NS', 'name': 'Voltas', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'VTL.NS', 'name': 'Vardhman Textiles', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'WABCOINDIA.NS', 'name': 'Wabco India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'WELCORP.NS', 'name': 'Welspun Corp', 'sector': 'metals', 'marketCap': 'micro'},
        {'symbol': 'WELSPUNIND.NS', 'name': 'Welspun India', 'sector': 'textiles', 'marketCap': 'micro'},
        {'symbol': 'WESTLIFE.NS', 'name': 'Westlife Foodworld', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'WHIRLPOOL.NS', 'name': 'Whirlpool of India', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'WOCKPHARMA.NS', 'name': 'Wockhardt', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'YESBANK.NS', 'name': 'Yes Bank', 'sector': 'banking', 'marketCap': 'micro'},
        {'symbol': 'ZENSARTECH.NS', 'name': 'Zensar Technologies', 'sector': 'it', 'marketCap': 'micro'},
        {'symbol': 'ZFCVINDIA.NS', 'name': 'ZF Commercial Vehicle Control Systems India', 'sector': 'auto', 'marketCap': 'micro'},
        {'symbol': 'ZYDUSLIFE.NS', 'name': 'Zydus Lifesciences', 'sector': 'healthcare', 'marketCap': 'micro'},
        {'symbol': 'ZOMATO.NS', 'name': 'Zomato', 'sector': 'consumer', 'marketCap': 'micro'},
        {'symbol': 'ZEEL.NS', 'name': 'Zee Entertainment Enterprises', 'sector': 'consumer', 'marketCap': 'micro'}
    ]

def get_stock_universe(universe_type):
    """Get stock universe - using only static lists (reliable)"""
    print(f"\n📋 Getting {universe_type} stock universe from static lists...")
    
    if universe_type == 'nifty50':
        stocks = get_nifty_50_stocks()
        print(f"✅ Got {len(stocks)} stocks for Nifty 50")
        return stocks
    
    elif universe_type == 'nifty100':
        stocks = get_nifty_100_stocks()
        print(f"✅ Got {len(stocks)} stocks for Nifty 100")
        return stocks
    
    elif universe_type == 'nifty200':
        stocks = get_nifty_200_stocks()
        print(f"✅ Got {len(stocks)} stocks for Nifty 200")
        return stocks
    elif universe_type == 'nifty500':
        stocks = get_nifty_500_stocks()
        print(f"✅ Got {len(stocks)} stocks for Nifty 500")
        return stocks
    else:
        # Default to Nifty 100
        return get_nifty_100_stocks()

def fetch_yahoo_finance_data(symbol):
    """Fetch real stock data from Yahoo Finance - ONLY working source"""
    print(f"🔍 Fetching REAL data from Yahoo Finance for {symbol}...")
    
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        params = {
            'range': '1mo',
            'interval': '1d',
            'includePrePost': 'true'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('chart') and data['chart'].get('result'):
                result = data['chart']['result'][0]
                
                timestamps = result['timestamp']
                indicators = result['indicators']['quote'][0]
                closes = indicators['close']
                
                # Remove None values and create valid data points
                valid_data = [(ts, close) for ts, close in zip(timestamps, closes) if close is not None]
                
                if len(valid_data) >= 7:  # Need at least a week of data
                    current_price = valid_data[-1][1]  # Latest price
                    
                    # Calculate dates for comparison
                    week_ago_ts = timestamps[-1] - (7 * 24 * 60 * 60)  # 7 days in seconds
                    month_ago_ts = timestamps[-1] - (30 * 24 * 60 * 60)  # 30 days in seconds
                    
                    # Find closest prices to our target dates
                    week_price = None
                    month_price = None
                    
                    for ts, price in valid_data:
                        if ts <= week_ago_ts:
                            week_price = price
                        if ts <= month_ago_ts:
                            month_price = price
                    
                    # Use earliest available if we don't have enough history
                    if week_price is None:
                        week_price = valid_data[0][1]
                    if month_price is None:
                        month_price = valid_data[0][1]
                    
                    # Calculate percentage changes
                    weekly_change = ((current_price - week_price) / week_price) * 100
                    monthly_change = ((current_price - month_price) / month_price) * 100
                    
                    # Get volume (latest non-null)
                    volumes = indicators.get('volume', [])
                    volume = 0
                    for v in reversed(volumes):
                        if v is not None and v > 0:
                            volume = int(v)
                            break
                    
                    print(f"✅ SUCCESS: Got real data for {symbol} - ₹{current_price:.2f}")
                    
                    return {
                        'symbol': symbol,
                        'currentPrice': round(current_price, 2),
                        'priceOneWeekAgo': round(week_price, 2),
                        'priceOneMonthAgo': round(month_price, 2),
                        'weeklyChange': round(weekly_change, 2),
                        'monthlyChange': round(monthly_change, 2),
                        'volume': volume,
                        'lastUpdated': datetime.now().isoformat(),
                        'status': 'success',
                        'source': 'yahoo_finance'
                    }
        
        print(f"❌ Yahoo Finance API failed for {symbol}: Status {response.status_code}")
        
    except Exception as e:
        print(f"❌ Yahoo Finance API error for {symbol}: {str(e)}")
    
    # If Yahoo Finance fails, return clear error
    return {
        'symbol': symbol,
        'error': 'Yahoo Finance API failed',
        'status': 'failed',
        'lastUpdated': datetime.now().isoformat(),
        'note': 'This stock will be excluded from scan results'
    }

# Flask Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Clean Stock Scanner - Yahoo Finance Only',
        'status': 'running',
        'version': '6.0 - Simplified & Clean',
        'policy': 'Real data only from Yahoo Finance',
        'universes': ['nifty50', 'nifty100', 'nifty200', 'nifty500'],
        'data_source': 'Yahoo Finance (Real market data)',
        'stock_source': 'Static curated lists (Reliable)',
        'endpoints': {
            '/stock-universe/<type>': 'Get stock universe (nifty50/nifty100/nifty200/nifty500)',
            '/scan': 'Scan stocks with real Yahoo Finance data',
            '/health': 'Health check'
        }
    })

@app.route('/stock-universe/<universe_type>')
def get_universe(universe_type):
    """Get stock universe by type"""
    try:
        stocks = get_stock_universe(universe_type)
        
        return jsonify({
            'universe_type': universe_type,
            'stocks': stocks,
            'total': len(stocks),
            'source': 'static_curated_list',
            'reliability': 'high',
            'timestamp': datetime.now().isoformat(),
            'message': f'Successfully got {len(stocks)} stocks for {universe_type}'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'universe_type': universe_type,
            'message': 'Failed to get stock universe'
        }), 500

@app.route('/scan', methods=['POST'])
def scan_stocks():
    """Scan stocks with Yahoo Finance data only"""
    try:
        data = request.get_json()
        
        # Get scan criteria
        weekly_threshold = float(data.get('weeklyThreshold', 5))
        monthly_threshold = float(data.get('monthlyThreshold', 10))
        market_cap_filter = data.get('marketCapFilter', 'all')
        sector_filter = data.get('sectorFilter', 'all')
        stock_universe = data.get('stockUniverse', 'nifty100')
        
        print(f"\n🔍 CLEAN SCAN STARTING")
        print(f"📊 Universe: {stock_universe}")
        print(f"🎯 Criteria: Weekly ≤ -{weekly_threshold}%, Monthly ≤ -{monthly_threshold}%")
        print(f"🏢 Filters: Market Cap = {market_cap_filter}, Sector = {sector_filter}")
        print(f"📈 Data Source: Yahoo Finance ONLY")
        
        # Get stock list
        stock_list = get_stock_universe(stock_universe)
        
        results = []
        processed = 0
        real_data_count = 0
        failed_count = 0
        
        for stock in stock_list:
            # Apply filters
            if market_cap_filter != 'all' and stock.get('marketCap') != market_cap_filter:
                continue
            if sector_filter != 'all' and stock.get('sector') != sector_filter:
                continue
            
            # Fetch REAL market data from Yahoo Finance
            market_data = fetch_yahoo_finance_data(stock['symbol'])
            processed += 1
            
            # Count data quality
            if market_data['status'] == 'success':
                real_data_count += 1
                
                # Check criteria
                weekly_decline = market_data['weeklyChange'] <= -weekly_threshold
                monthly_decline = market_data['monthlyChange'] <= -monthly_threshold
                
                if weekly_decline and monthly_decline:
                    result = {**stock, **market_data}
                    results.append(result)
                    print(f"✅ MATCH: {stock['symbol']} - W:{market_data['weeklyChange']}% M:{market_data['monthlyChange']}% [YAHOO FINANCE]")
                    
            else:  # failed
                failed_count += 1
                print(f"❌ FAILED: {stock['symbol']} - Yahoo Finance API failed")
            
            # Delay to respect API limits
            time.sleep(1)
            
            # Progress update every 10 stocks
            if processed % 10 == 0:
                print(f"\n📊 Progress: {processed}/{len(stock_list)}")
                print(f"   ✅ Yahoo Finance success: {real_data_count}")
                print(f"   ❌ Failed: {failed_count}")
                print(f"   🎯 Matches found: {len(results)}")
        
        print(f"\n🎯 SCAN COMPLETE:")
        print(f"   📊 Universe: {stock_universe} ({len(stock_list)} stocks)")
        print(f"   📈 Processed: {processed}")
        print(f"   ✅ Yahoo Finance success: {real_data_count}")
        print(f"   ❌ Failed: {failed_count}")
        print(f"   🎯 Stocks meeting criteria: {len(results)}")
        
        return jsonify({
            'results': results,
            'total_matches': len(results),
            'stock_universe': stock_universe,
            'universe_size': len(stock_list),
            'processed': processed,
            'yahoo_finance_success': real_data_count,
            'failed_count': failed_count,
            'success_rate': f"{((real_data_count / processed) * 100):.1f}%" if processed > 0 else "0%",
            'criteria': {
                'weeklyThreshold': weekly_threshold,
                'monthlyThreshold': monthly_threshold,
                'marketCapFilter': market_cap_filter,
                'sectorFilter': sector_filter,
                'stockUniverse': stock_universe
            },
            'data_source': 'Yahoo Finance (Real market data)',
            'stock_source': 'Static curated lists',
            'policy': 'Real data only - no simulation',
            'timestamp': datetime.now().isoformat(),
            'message': f'Scanned {stock_universe}: {len(results)} declining stocks found from {real_data_count} successful Yahoo Finance calls'
        })
        
    except Exception as e:
        print(f"❌ Scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '6.0',
        'features': ['Clean & Simple', 'Yahoo Finance Only', 'Static Curated Lists'],
        'data_source': 'Yahoo Finance API',
        'stock_source': 'Static Lists (50-450+ stocks)',
        'reliability': 'High - No external dependencies',
        'universes_available': ['nifty50', 'nifty100', 'nifty200', 'nifty500'],
        'message': 'Clean Stock Scanner ready - Yahoo Finance + Static Lists'
    })

@app.route('/test-stock/<symbol>')
def test_stock(symbol):
    """Test Yahoo Finance data for specific stock"""
    if not symbol.endswith('.NS'):
        symbol += '.NS'
    
    data = fetch_yahoo_finance_data(symbol)
    return jsonify({
        'symbol': symbol,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = not (os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'))
    environment = "Production (Railway)" if (os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')) else "Development"
    
    app.run(debug=debug, host='0.0.0.0', port=port)