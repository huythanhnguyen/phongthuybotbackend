// Test script for Phong Thủy Số API

const axios = require('axios');

// Base URL of the API
const API_URL = 'https://phongthuybotbackend.onrender.com';

async function testAPI() {
  try {
    console.log('🧪 Starting API tests...');

    // Test 1: Root endpoint
    console.log('\n📌 Test 1: Root endpoint');
    const rootResponse = await axios.get(API_URL);
    console.log('Status:', rootResponse.status);
    console.log('Data:', JSON.stringify(rootResponse.data, null, 2));

    // Test 2: Health check endpoint
    console.log('\n📌 Test 2: Health check endpoint');
    const healthResponse = await axios.get(`${API_URL}/api/health`);
    console.log('Status:', healthResponse.status);
    console.log('Data:', JSON.stringify(healthResponse.data, null, 2));

    // Test 3: Bát Cục Linh Số info endpoint
    console.log('\n📌 Test 3: Bát Cục Linh Số info endpoint');
    const bclsResponse = await axios.get(`${API_URL}/api/v2/bat-cuc-linh-so`);
    console.log('Status:', bclsResponse.status);
    console.log('Data:', JSON.stringify(bclsResponse.data, null, 2));

    // Test 4: Analyze phone number
    console.log('\n📌 Test 4: Analyze phone number');
    const phoneResponse = await axios.post(`${API_URL}/api/v2/bat-cuc-linh-so/phone`, {
      phoneNumber: '0987654321'
    });
    console.log('Status:', phoneResponse.status);
    console.log('Data:', JSON.stringify(phoneResponse.data, null, 2));

    // Test 5: Analyze CCCD
    console.log('\n📌 Test 5: Analyze CCCD');
    const cccdResponse = await axios.post(`${API_URL}/api/v2/bat-cuc-linh-so/cccd`, {
      cccdNumber: '012345678901'
    });
    console.log('Status:', cccdResponse.status);
    console.log('Data:', JSON.stringify(cccdResponse.data, null, 2));

    // Test 6: Root Agent info endpoint
    console.log('\n📌 Test 6: Root Agent info endpoint');
    const agentResponse = await axios.get(`${API_URL}/api/v2/agent`);
    console.log('Status:', agentResponse.status);
    console.log('Data:', JSON.stringify(agentResponse.data, null, 2));

    // Test 7: Chat with Root Agent
    console.log('\n📌 Test 7: Chat with Root Agent');
    const chatResponse = await axios.post(`${API_URL}/api/v2/agent/chat`, {
      message: 'Phân tích số điện thoại 0987654321'
    });
    console.log('Status:', chatResponse.status);
    console.log('Data:', JSON.stringify(chatResponse.data, null, 2));

    console.log('\n✅ All tests completed!');
  } catch (error) {
    console.error('❌ Error during testing:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

// Run the tests
testAPI(); 