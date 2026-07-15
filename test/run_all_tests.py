"""
LifeStarway 全量测试运行脚本
运行后端 pytest 测试 + 前端 Node.js 测试，汇总生成报告
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
TEST_DIR = PROJECT_ROOT / "test"
BACKEND_TEST_DIR = TEST_DIR / "backend"
FRONTEND_TEST_DIR = TEST_DIR / "frontend"
VENV_PYTHON = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"


def run_backend_tests():
    """运行后端 pytest 测试"""
    print("\n" + "═" * 60)
    print("  后端测试 (pytest)")
    print("═" * 60)

    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

    # 确保测试依赖已安装
    subprocess.run(
        [python_exe, "-m", "pip", "install", "-q",
         "pytest", "pytest-asyncio", "httpx", "aiosqlite"],
        cwd=str(BACKEND_DIR),
        capture_output=True,
    )

    result = subprocess.run(
        [python_exe, "-m", "pytest",
         str(BACKEND_TEST_DIR),
         "-v",
         "--tb=short",
         f"--rootdir={BACKEND_TEST_DIR}",
         f"-c={BACKEND_TEST_DIR / 'pytest.ini'}"],
        cwd=str(BACKEND_DIR),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(BACKEND_DIR)},
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:2000])

    # 解析 pytest 输出
    passed = result.stdout.count(" PASSED")
    failed = result.stdout.count(" FAILED")
    errors = result.stdout.count(" ERROR")

    return {
        "suite": "后端测试",
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": passed + failed + errors,
        "exit_code": result.returncode,
        "raw_output": result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout,
    }


def run_frontend_tests():
    """运行前端测试"""
    print("\n" + "═" * 60)
    print("  前端测试 (Node.js)")
    print("═" * 60)

    result = subprocess.run(
        ["node", str(FRONTEND_TEST_DIR / "test_frontend.js")],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:2000])

    # 尝试读取 JSON 报告
    report_path = FRONTEND_TEST_DIR / "frontend_test_report.json"
    if report_path.exists():
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        return {
            "suite": "前端测试",
            "passed": report.get("passed", 0),
            "failed": report.get("failed", 0),
            "errors": 0,
            "total": report.get("total_tests", 0),
            "exit_code": result.returncode,
            "raw_output": result.stdout[-2000:],
        }

    return {
        "suite": "前端测试",
        "passed": 0,
        "failed": 0,
        "errors": 1,
        "total": 0,
        "exit_code": result.returncode,
        "raw_output": result.stderr[:1000],
    }


def generate_report(backend_result, frontend_result):
    """生成汇总测试报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_passed = backend_result["passed"] + frontend_result["passed"]
    total_failed = backend_result["failed"] + frontend_result["failed"]
    total_errors = backend_result["errors"] + frontend_result["errors"]
    total_tests = backend_result["total"] + frontend_result["total"]

    report = {
        "project": "LifeStarway 人生星途",
        "date": timestamp,
        "summary": {
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "errors": total_errors,
            "pass_rate": f"{(total_passed / total_tests * 100):.1f}%" if total_tests > 0 else "0%",
        },
        "suites": [backend_result, frontend_result],
    }

    report_path = TEST_DIR / "test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 打印汇总
    print("\n" + "═" * 60)
    print("  LifeStarway 全量测试报告")
    print("═" * 60)
    print(f"  日期: {timestamp}")
    print(f"  总测试数: {total_tests}")
    print(f"  通过: {total_passed}")
    print(f"  失败: {total_failed}")
    print(f"  错误: {total_errors}")
    print(f"  通过率: {report['summary']['pass_rate']}")
    print("─" * 60)
    for suite in report["suites"]:
        status = "✓ 全部通过" if suite["exit_code"] == 0 else "✗ 有失败项"
        print(f"  {suite['suite']}: {suite['passed']}/{suite['total']} 通过 {status}")
    print("═" * 60)
    print(f"\n  报告已保存到: {report_path}")

    return total_failed + total_errors


def main():
    """主入口"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "  LifeStarway 全量测试".center(46) + "║")
    print("╚" + "═" * 58 + "╝")

    start_time = time.time()

    # 运行后端测试
    backend_result = run_backend_tests()

    # 运行前端测试
    frontend_result = run_frontend_tests()

    # 生成报告
    failed_count = generate_report(backend_result, frontend_result)

    elapsed = time.time() - start_time
    print(f"  耗时: {elapsed:.1f}s")

    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
