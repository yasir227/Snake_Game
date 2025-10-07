#!/usr/bin/env python3
"""
Setup Test Script for Snake Game Portfolio Project
==================================================

This script verifies that all dependencies are properly installed
and the project is ready to run. Perfect for employers or contributors
to quickly validate the setup.

Run this before playing the game to ensure everything works!
"""

import sys
import os
import json
from importlib import import_module

def test_python_version():
    """Test if Python version is compatible."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Needs Python 3.8+")
        return False

def test_dependencies():
    """Test if all required packages are installed."""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('pygame', 'Game engine'),
        ('pandas', 'Data analysis'),
        ('matplotlib', 'Data visualization'),
        ('numpy', 'Numerical computing'),
    ]
    
    all_good = True
    
    for package, description in dependencies:
        try:
            import_module(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} (MISSING)")
            all_good = False
    
    return all_good

def test_project_structure():
    """Test if project structure is correct."""
    print("\n📁 Testing project structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'config/settings.json',
        'src/game.py',
        'src/snake.py',
        'src/food.py',
        'src/game_stats.py',
        'src/data_visualizer.py'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (MISSING)")
            all_good = False
    
    return all_good

def test_configuration():
    """Test if configuration file is valid."""
    print("\n⚙️ Testing configuration...")
    
    try:
        with open('config/settings.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['game', 'data', 'features']
        for key in required_keys:
            if key in config:
                print(f"   ✅ Config section '{key}' found")
            else:
                print(f"   ❌ Config section '{key}' missing")
                return False
        
        print("   ✅ Configuration file is valid!")
        return True
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_game_import():
    """Test if game modules can be imported."""
    print("\n🎮 Testing game modules...")
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from game import SnakeGame
        from snake import Snake
        from food import Food
        from game_stats import GameStats
        from data_visualizer import GameDataVisualizer
        
        print("   ✅ All game modules imported successfully!")
        return True
    
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def run_complete_test():
    """Run all tests and provide summary."""
    print("="*60)
    print("🐍 SNAKE GAME PORTFOLIO - SETUP TEST")
    print("="*60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Project Structure", test_project_structure),
        ("Configuration", test_configuration),
        ("Game Modules", test_game_import)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("Your Snake Game is ready to run!")
        print("\nTo start playing:")
        print("   python main.py")
        print("\nTo view analytics:")
        print("   python src/data_visualizer.py")
        return True
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    run_complete_test()